import enum
import logging
from datetime import timedelta
from typing import Dict, Optional, Union
from dataclasses import dataclass

import yaml
from certvalidator import ValidationContext
from pyhanko.pdf_utils.config_utils import (
    check_config_keys, ConfigurationError
)
from pyhanko.pdf_utils.misc import get_and_apply
from pyhanko.sign import signers


# TODO add stamp styles etc.
from pyhanko.sign.signers import DEFAULT_SIGNING_STAMP_STYLE
from pyhanko.stamp import QRStampStyle, TextStampStyle


class StdLogOutput(enum.Enum):
    STDERR = enum.auto()
    STDOUT = enum.auto()


@dataclass(frozen=True)
class LogConfig:
    level: Union[int, str]
    """
    Logging level, should be one of the levels defined in the logging module.
    """

    output: Union[StdLogOutput, str]
    """
    Name of the output file, or a standard one.
    """

    @staticmethod
    def parse_output_spec(spec) -> Union[StdLogOutput, str]:
        if not isinstance(spec, str):
            raise ConfigurationError(
                "Log output must be specified as a string."
            )
        spec_l = spec.lower()
        if spec_l == 'stderr':
            return StdLogOutput.STDERR
        elif spec_l == 'stdout':
            return StdLogOutput.STDOUT
        else:
            return spec


@dataclass
class CLIConfig:
    validation_contexts: Dict[str, dict]
    stamp_styles: Dict[str, dict]
    default_validation_context: str
    default_stamp_style: str
    time_tolerance: timedelta
    log_config: Dict[Optional[str], LogConfig]

    # TODO graceful error handling

    def get_validation_context(self, name=None, as_dict=False):
        name = name or self.default_validation_context
        try:
            vc_config = self.validation_contexts[name]
        except KeyError:
            raise ConfigurationError(
                f"There is no validation context named '{name}'."
            )
        vc_kwargs = parse_trust_config(vc_config, self.time_tolerance)
        return vc_kwargs if as_dict else ValidationContext(**vc_kwargs)

    def get_stamp_style(self, name=None) -> TextStampStyle:
        name = name or self.default_stamp_style
        try:
            style_config = dict(self.stamp_styles[name])
        except KeyError:
            raise ConfigurationError(
                f"There is no stamp style named '{name}'."
            )
        except TypeError as e:
            raise ConfigurationError(e)
        cls = STAMP_STYLE_TYPES[style_config.pop('type', 'text')]
        return cls.from_config(style_config)


def init_validation_context_kwargs(trust, trust_replace, other_certs,
                                   time_tolerance=None):
    vc_kwargs = {
        'time_tolerance':
            timedelta(seconds=DEFAULT_TIME_TOLERANCE) if time_tolerance is None
            else time_tolerance
    }
    if trust:
        if isinstance(trust, str):
            trust = (trust,)
        # add trust roots to the validation context, or replace them
        trust_certs = list(signers.load_certs_from_pemder(trust))
        if trust_replace:
            vc_kwargs['trust_roots'] = trust_certs
        else:
            vc_kwargs['extra_trust_roots'] = trust_certs
    if other_certs:
        if isinstance(other_certs, str):
            other_certs = (other_certs,)
        vc_kwargs['other_certs'] = list(
            signers.load_certs_from_pemder(other_certs)
        )
    return vc_kwargs


# TODO allow CRL/OCSP loading here as well (esp. CRL loading might be useful
#  in some cases)
# Time-related settings are probably better off in the CLI.

def parse_trust_config(trust_config, time_tolerance) -> dict:
    check_config_keys(
        'ValidationContext', ('trust', 'trust-replace', 'other-certs'),
        trust_config
    )
    return init_validation_context_kwargs(
        trust=trust_config.get('trust'),
        trust_replace=trust_config.get('trust-replace', False),
        other_certs=trust_config.get('other-certs'),
        time_tolerance=time_tolerance
    )


DEFAULT_ROOT_LOGGER_LEVEL = logging.INFO


def _retrieve_log_level(settings_dict, key, default=None) -> Union[int, str]:
    try:
        level_spec = settings_dict[key]
    except KeyError:
        if default is not None:
            return default
        raise ConfigurationError(
            f"Logging config for '{key}' does not define a log level."
        )
    if not isinstance(level_spec, (int, str)):
        raise ConfigurationError(
            f"Log levels must be int or str, not {type(level_spec)}"
        )
    return level_spec


def parse_logging_config(log_config_spec) -> Dict[Optional[str], LogConfig]:
    if not isinstance(log_config_spec, dict):
        raise ConfigurationError('logging config should be a dictionary')

    root_logger_level = _retrieve_log_level(
        log_config_spec, 'root-level', default=DEFAULT_ROOT_LOGGER_LEVEL
    )

    root_logger_output = get_and_apply(
        log_config_spec, 'root-output', LogConfig.parse_output_spec,
        default=StdLogOutput.STDERR
    )

    log_config = {None: LogConfig(root_logger_level, root_logger_output)}

    logging_by_module = log_config_spec.get('by-module', {})
    if not isinstance(logging_by_module, dict):
        raise ConfigurationError('logging.by-module should be a dict')

    for module, module_logging_settings in logging_by_module.items():
        if not isinstance(module, str):
            raise ConfigurationError(
                "Keys in logging.by-module should be strings"
            )
        level_spec = _retrieve_log_level(module_logging_settings, 'level')
        output_spec = get_and_apply(
            module_logging_settings, 'output', LogConfig.parse_output_spec,
            default=StdLogOutput.STDERR
        )
        log_config[module] = LogConfig(level=level_spec, output=output_spec)

    return log_config


DEFAULT_VALIDATION_CONTEXT = DEFAULT_STAMP_STYLE = 'default'
DEFAULT_TIME_TOLERANCE = 10
STAMP_STYLE_TYPES = {
    'qr': QRStampStyle,
    'text': TextStampStyle,
}


def parse_cli_config(yaml_str):
    config_dict = yaml.safe_load(yaml_str) or {}

    # validation context config
    vcs = {DEFAULT_VALIDATION_CONTEXT: {}}
    try:
        vc_specs = config_dict['validation-contexts']
        vcs.update(vc_specs)
    except KeyError:
        pass

    # stamp style config
    # TODO this style is obviously not suited for non-signing scenarios
    #  (but it'll do for now)
    stamp_configs = {DEFAULT_STAMP_STYLE: DEFAULT_SIGNING_STAMP_STYLE}
    try:
        stamp_specs = config_dict['stamp-styles']
        stamp_configs.update(stamp_specs)
    except KeyError:
        pass

    # logging config
    log_config_spec = config_dict.get('logging', {})
    log_config = parse_logging_config(log_config_spec)

    # some misc settings
    default_vc = config_dict.get(
        'default-validation-context', DEFAULT_VALIDATION_CONTEXT
    )
    default_stamp_style = config_dict.get(
        'default-stamp-style', DEFAULT_STAMP_STYLE
    )
    time_tolerance = timedelta(
        seconds=config_dict.get('time-tolerance', DEFAULT_TIME_TOLERANCE)
    )
    return CLIConfig(
        validation_contexts=vcs, default_validation_context=default_vc,
        time_tolerance=time_tolerance, stamp_styles=stamp_configs,
        default_stamp_style=default_stamp_style,
        log_config=log_config
    )
