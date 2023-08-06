import json
import os
import sys
import re

import logging
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError, TemplateNotFound, UndefinedError
import arrow
import fnmatch

from .exceptions import FormicaArgumentException

from . import yaml_tags
from .helper import main_account_id

# To silence pyflakes warning of unused import
assert yaml_tags

logger = logging.getLogger(__name__)

FILE_TYPES = ["yml", "yaml", "json"]

RESOURCES_KEY = "Resources"
MODULE_KEY = "From"

ALLOWED_ATTRIBUTES = {
    "AWSTemplateFormatVersion": [str],
    "Description": [str],
    "Metadata": dict,
    "Parameters": dict,
    "Mappings": dict,
    "Conditions": dict,
    "Transform": [str, list],
    RESOURCES_KEY: dict,
    "Outputs": dict,
}


def code_escape(source):
    return source.replace("\n", "\\n").replace('"', '\\"')


def code_array(source):
    lines = source.split("\\n")
    return "[" + ",".join(['"%s"' % line for line in lines]) + "]"


def mandatory(a):
    from jinja2.runtime import Undefined

    if isinstance(a, Undefined) or a is None:
        raise FormicaArgumentException("Mandatory variable not set.")
    return a


def resource(name):
    if name is None:
        return ""
    else:
        return "".join(e for e in name.title() if e.isalnum())


def novalue(variable):
    return variable or '{"Ref": "AWS::NoValue"}'


class Loader(object):
    def __init__(self, path=".", filename="*", variables=None, main_account_parameter=False):
        if variables is None:
            variables = {}
        self.cftemplate = {}
        self.path = path
        self.filename = filename
        self.env = Environment(loader=FileSystemLoader("./", followlinks=True))
        self.env.filters.update(
            {
                "code_escape": code_escape,
                "code_array": code_array,
                "mandatory": mandatory,
                "resource": resource,
                "novalue": novalue,
            }
        )
        self.variables = variables
        self.main_account_parameter = main_account_parameter

    def include_file(self, filename, **args):
        source = self.render(filename, **args)
        return code_escape(source)

    def load_file(self, filename, **args):
        return self.render(filename, **args)

    def list_files(self, filter="*"):
        return [t for t in self.env.list_templates() if fnmatch.fnmatch(t, filter)]

    def render(self, filename, **args):
        template_path = os.path.normpath("{}/{}".format(self.path, filename))
        template = self.env.get_template(template_path)
        variables = {}
        variables.update(self.variables)
        variables.update(args)
        arguments = dict(
            code=self.include_file,
            file=self.load_file,
            files=self.list_files,
            now=arrow.now,
            utcnow=arrow.utcnow,
            **variables,
        )
        return template.render(**arguments)

    def template(self, indent=4, sort_keys=True, separators=(",", ":"), dumper=None):
        if dumper is not None:
            return dumper(self.cftemplate)
        return json.dumps(self.cftemplate, indent=indent, sort_keys=sort_keys, separators=separators)

    def template_dictionary(self):
        return self.cftemplate

    def merge(self, template, file):
        if template:
            for key in template.keys():
                new = template[key]
                new_type = type(new)
                types = ALLOWED_ATTRIBUTES.get(key)
                if type(types) != list:
                    types = [types]
                if key in ALLOWED_ATTRIBUTES.keys() and new_type in types:
                    if new_type == str or new_type == list:
                        self.cftemplate[key] = new
                    elif new_type == dict:
                        for element_key, element_value in template[key].items():
                            if (
                                key == RESOURCES_KEY
                                and isinstance(element_value, dict)
                                and MODULE_KEY in element_value
                            ):
                                self.load_module(element_value[MODULE_KEY], element_key, element_value)
                            else:
                                self.cftemplate.setdefault(key, {})[element_key] = element_value
                else:
                    logger.info("Key '{}' in file {} is not valid".format(key, file))
                    sys.exit(1)
        else:
            logger.info("File {} is empty".format(file))

    def load_module(self, module_path, element_key, element_value):
        path_elements = module_path.split("::")
        dir_pattern = re.compile(fnmatch.translate(path_elements.pop(0)), re.IGNORECASE)
        matched_dirs = [dir for dir in os.listdir(self.path) if dir_pattern.match(dir)]
        matched_dir = module_path
        if matched_dirs:
            matched_dir = matched_dirs[0]

        module_path = self.path + "/" + "/".join([matched_dir] + path_elements)

        file_name = "*"

        if not os.path.isdir(module_path):
            file_name = module_path.split("/")[-1]
            module_path = "/".join(module_path.split("/")[:-1])

        properties = element_value.get("Properties", {})
        properties["module_name"] = element_key
        vars = self.merge_variables(properties)

        loader = Loader(module_path, file_name, vars)
        loader.load()
        self.merge(loader.template_dictionary(), file=file_name)

    def merge_variables(self, module_vars):
        merged_vars = {}
        for k, v in self.variables.items():
            merged_vars[k] = v
        for k, v in module_vars.items():
            merged_vars[k] = v
        return merged_vars

    def load(self):
        files = []

        for file_type in FILE_TYPES:
            pattern = re.compile(fnmatch.translate("{}.template.{}".format(self.filename, file_type)), re.IGNORECASE)
            files.extend([filename for filename in os.listdir(self.path) if pattern.match(filename)])

        if not files:
            logger.info("Could not find any template files in {}".format(self.path))
            sys.exit(1)

        for file in files:
            try:
                result = str(self.render(os.path.basename(file), **self.variables))
                template = yaml.full_load(result)
            except TemplateNotFound as e:
                logger.info("File not found" + ": " + e.message)
                logger.info('In: "' + file + '"')
                sys.exit(1)
            except TemplateSyntaxError as e:
                logger.info(e.__class__.__name__ + ": " + e.message)
                logger.info('File: "' + (e.filename or file) + '", line ' + str(e.lineno))
                sys.exit(1)
            except UndefinedError as e:
                logger.info(e.__class__.__name__ + ": " + e.message)
                logger.info('In: "' + file + '"')
                sys.exit(1)
            except FormicaArgumentException as e:
                logger.info(e.__class__.__name__ + ": " + e.args[0])
                logger.info('For Template: "' + file + '"')
                logger.info("If you use it as a template make sure you're setting all necessary vars")
                sys.exit(1)
            except yaml.YAMLError as e:
                logger.info(e.__str__())
                logger.info("Following is the Yaml document formica is trying to load:")
                logger.info("---------------------------------------------------------------------------")
                logger.info(result)
                logger.info("---------------------------------------------------------------------------")
                sys.exit(1)
            self.merge(template, file)

        if self.main_account_parameter:
            self.cftemplate["Parameters"] = self.cftemplate.get("Parameters") or {}
            self.cftemplate["Parameters"]["MainAccount"] = {"Type": "String", "Default": main_account_id()}
