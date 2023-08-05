# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

import json
import shutil

from tsfpga import TSFPGA_TCL
from tsfpga.system_utils import create_file, read_file
from tsfpga.build_step_tcl_hook import BuildStepTclHook
from .common import run_vivado_tcl, run_vivado_gui
from .size_checker import UtilizationParser
from .tcl import VivadoTcl


class VivadoProject:
    """
    Used for handling a Xilinx Vivado HDL project
    """

    # pylint: disable=too-many-arguments,too-many-instance-attributes
    def __init__(
        self,
        name,
        modules,
        part,
        top=None,
        generics=None,
        constraints=None,
        tcl_sources=None,
        build_step_hooks=None,
        vivado_path=None,
        default_run_index=1,
        defined_at=None,
    ):
        """
        Arguments:
            name (str): Project name.
            modules (list(:class:`Module <.BaseModule>`)): Modules that shall be included in the
                project.
            part (str): Part identification.
            top (str): Name of top level entity. If left out, the top level name will be
                inferred from the ``name``.
            generics: A dict with generics values (`dict(name: value)`). Use this parameter
                for "static" generics that do not change between multiple builds of this
                project. These will be set in the project when it is created.

                Compare to the build-time generic argument in :meth:`build`.
            constraints (list(Constraint)): Constraints that will be applied to the project.
            tcl_sources (list(`pathlib.Path`)): A list of TCL files. Use for e.g. block design,
                pinning, settings, etc.
            build_step_hooks (list(BuildStepTclHook)): Build step hooks that will be applied to the
                project.
            vivado_path (`pathlib.Path`): A path to the Vivado executable. If omitted,
                the default location from the system PATH will be used.
            default_run_index (int): Default run index (synth_X and impl_X) that is set in the
                project. Can also use the argument to :meth:`build() <VivadoProject.build>` to
                specify at build-time.
            defined_at (`pathlib.Path`): Optional path to the file where you defined your
                project. To get a useful ``build.py --list`` message. Is useful when you have many
                projects set up.
        """
        self.name = name
        self.modules = modules
        self.part = part
        self.static_generics = None if generics is None else generics.copy()
        self.constraints = constraints
        self.default_run_index = default_run_index
        self.defined_at = defined_at

        # Will be set by child class when applicable
        self.is_netlist_build = False
        self.analyze_clock_interaction = True

        self.top = name + "_top" if top is None else top
        self._vivado_path = vivado_path

        self._setup_tcl_sources_list(tcl_sources)
        self._setup_build_step_hooks(build_step_hooks)

        self.tcl = VivadoTcl(name=self.name)

    def _setup_tcl_sources_list(self, tcl_sources_from_user):
        tsfpga_tcl_sources = [
            TSFPGA_TCL / "vivado_default_run.tcl",
            TSFPGA_TCL / "vivado_fast_run.tcl",
            TSFPGA_TCL / "vivado_messages.tcl",
        ]
        # Note that the list concatenation below does a (shallow) copy of the lists
        user_tcl_sources = [] if tcl_sources_from_user is None else tcl_sources_from_user

        # Add tsfpga TCL sources first. The user might want to change something in the tsfpga
        # settings. Conversely, tsfpga should not modify something that the user has set up.
        self.tcl_sources = tsfpga_tcl_sources + user_tcl_sources

    def _setup_build_step_hooks(self, build_step_hooks_from_user):
        # Lists are mutable. Since we assign and modify this one we have to copy it.
        self.build_step_hooks = (
            [] if build_step_hooks_from_user is None else build_step_hooks_from_user.copy()
        )

        self.build_step_hooks.append(
            BuildStepTclHook(
                TSFPGA_TCL / "vivado_report_utilization.tcl", "STEPS.SYNTH_DESIGN.TCL.POST"
            )
        )
        self.build_step_hooks.append(
            BuildStepTclHook(
                TSFPGA_TCL / "vivado_report_utilization.tcl", "STEPS.WRITE_BITSTREAM.TCL.PRE"
            )
        )
        self.build_step_hooks.append(
            BuildStepTclHook(
                TSFPGA_TCL / "vivado_check_timing.tcl", "STEPS.WRITE_BITSTREAM.TCL.PRE"
            )
        )

    def project_file(self, project_path):
        """
        Arguments:
            project_path (`pathlib.Path`): A path containing a Vivado project.
        Return:
            `pathlib.Path`: The project file of this project, in the given folder
        """
        return project_path / (self.name + ".xpr")

    def _create_tcl(self, project_path, ip_cache_path):
        """
        Make a TCL file that creates a Vivado project
        """
        if project_path.exists():
            raise ValueError(f"Folder already exists: {project_path}")
        project_path.mkdir(parents=True)

        create_vivado_project_tcl = project_path / "create_vivado_project.tcl"
        tcl = self.tcl.create(
            project_folder=project_path,
            modules=self.modules,
            part=self.part,
            top=self.top,
            run_index=self.default_run_index,
            generics=self.static_generics,
            constraints=self.constraints,
            tcl_sources=self.tcl_sources,
            build_step_hooks=self.build_step_hooks,
            ip_cache_path=ip_cache_path,
            disable_io_buffers=self.is_netlist_build,
        )
        create_file(create_vivado_project_tcl, tcl)

        return create_vivado_project_tcl

    def create(self, project_path, ip_cache_path=None):
        """
        Create a Vivado project

        Arguments:
            project_path (`pathlib.Path`): Path where the project shall be placed.
            ip_cache_path (`pathlib.Path`): Path to a folder where the Vivado IP cache can be
                placed. If omitted, the Vivado IP cache mechanism will not be enabled.

        Returns:
            bool: True if everything went well.
        """
        print(f"Creating Vivado project in {project_path}")
        if not self.pre_create(project_path=project_path, ip_cache_path=ip_cache_path):
            print("ERROR: Project pre-create hook returned False. Failing the build.")
            return False

        create_vivado_project_tcl = self._create_tcl(project_path, ip_cache_path)
        return run_vivado_tcl(self._vivado_path, create_vivado_project_tcl)

    def pre_create(self, **kwargs):  # pylint: disable=no-self-use, unused-argument
        """
        Override this function in a child class if you wish to do something useful with it.
        Will be called from :meth:`.create` right before the call to Vivado.

        An example use case for this function is when TCL source scripts for the Vivado project
        have to be auto generated. This could e.g. be scripts that set IP repo paths based on the
        Vivado system PATH.

        .. Note::
            This default method does nothing. Shall be overridden by project that utilize
            this mechanism.

        Arguments:
            kwargs: Will have all the :meth:`.create` parameters in it.

        Return:
            bool: True if everything went well.
        """
        return True

    def _build_tcl(self, project_path, output_path, num_threads, run_index, generics, synth_only):
        """
        Make a TCL file that builds a Vivado project
        """
        project_file = self.project_file(project_path)
        if not project_file.exists():
            raise ValueError(
                f"Project file does not exist in the specified location: {project_file}"
            )

        if self.static_generics is None:
            all_generics = generics
        elif generics is None:
            all_generics = self.static_generics
        else:
            # Add the two dictionaries
            all_generics = self.static_generics.copy()
            all_generics.update(generics)

        build_vivado_project_tcl = project_path / "build_vivado_project.tcl"
        tcl = self.tcl.build(
            project_file=project_file,
            output_path=output_path,
            num_threads=num_threads,
            run_index=run_index,
            generics=all_generics,
            synth_only=synth_only,
            analyze_clock_interaction=self.analyze_clock_interaction,
        )
        create_file(build_vivado_project_tcl, tcl)

        return build_vivado_project_tcl

    def pre_build(self, **kwargs):  # pylint: disable=no-self-use, unused-argument
        """
        Override this function in a child class if you wish to do something useful with it.
        Will be called from :meth:`.build` right before the call to Vivado.

        Arguments:
            kwargs: Will have all the :meth:`.build` parameters in it. Including additional
                parameters from the user.

        Return:
            bool: True if everything went well.
        """
        return True

    def post_build(self, **kwargs):  # pylint: disable=no-self-use, unused-argument
        """
        Override this function in a child class if you wish to do something useful with it.
        Will be called from :meth:`.build` right after the call to Vivado.

        An example use case for this function is to encrypt the bit file, or generate any other
        material that shall be included in FPGA release artifacts.

        .. Note::
            This default method does nothing. Shall be overridden by project that utilize
            this mechanism.

        Arguments:
            kwargs: Will have all the :meth:`.build` parameters in it. Including additional
                parameters from the user. Will also include ``build_result`` with
                implemented/synthesized size, which can be used for asserting the expected resource
                utilization.

        Return:
            bool: True if everything went well.
        """
        return True

    def build(
        self,
        project_path,
        output_path=None,
        run_index=None,
        generics=None,
        synth_only=False,
        num_threads=12,
        **pre_and_post_build_parameters,
    ):
        """
        Build a Vivado project

        Arguments:
            project_path (`pathlib.Path`): A path containing a Vivado project.
            output_path (`pathlib.Path`): Results (bit file, ...) will be placed here.
            run_index (int): Select Vivado run (synth_X and impl_X) to build with.
            generics: A dict with generics values (`dict(name: value)`). Use for run-time
                generics, i.e. values that can change between each build of this project.

                Compare to the create-time generics argument in :meth:`.__init__`.
            synth_only (bool): Run synthesis and then stop.
            num_threads (int): Number of parallel threads to use during run.
            pre_and_post_build_parameters: Additional parameters that will be
                sent to :meth:`.pre_build` and :meth:`.post_build` functions.

                .. note::
                    This is a "kwargs" style argument. You can pass any number of named arguments.

        Return:
            BuildResult: Result object with build information.
        """
        synth_only = synth_only or self.is_netlist_build

        if output_path is None and not synth_only:
            raise ValueError("Must specify output_path when doing an implementation run")

        if synth_only:
            print(f"Synthesizing Vivado project in {project_path}")
        else:
            print(f"Building Vivado project in {project_path}, placing artifacts in {output_path}")

        # Run index is optional to specify at build-time
        run_index = self.default_run_index if run_index is None else run_index

        # Send all available information to pre- and post build functions
        pre_and_post_build_parameters.update(
            project_path=project_path,
            output_path=output_path,
            run_index=run_index,
            generics=generics,
            synth_only=synth_only,
            num_threads=num_threads,
        )

        result = BuildResult(self.name)

        for module in self.modules:
            if not module.pre_build(project=self, **pre_and_post_build_parameters):
                print(
                    f"ERROR: Module {module.name} pre-build hook returned False. Failing the build."
                )
                result.success = False
                return result

            # Make sure register packages are up to date
            module.create_regs_vhdl_package()

        if not self.pre_build(**pre_and_post_build_parameters):
            print("ERROR: Project pre-build hook returned False. Failing the build.")
            result.success = False
            return result

        build_vivado_project_tcl = self._build_tcl(
            project_path=project_path,
            output_path=output_path,
            num_threads=num_threads,
            run_index=run_index,
            generics=generics,
            synth_only=synth_only,
        )

        if not run_vivado_tcl(self._vivado_path, build_vivado_project_tcl):
            result.success = False
            return result

        result.synthesis_size = self._get_size(project_path, f"synth_{run_index}")

        if not synth_only:
            impl_folder = project_path / f"{self.name}.runs" / f"impl_{run_index}"
            shutil.copy2(impl_folder / f"{self.top}.bit", output_path / f"{self.name}.bit")
            shutil.copy2(impl_folder / f"{self.top}.bin", output_path / f"{self.name}.bin")
            result.implementation_size = self._get_size(project_path, f"impl_{run_index}")

        # Send the result object, along with everything else, to the post-build function
        pre_and_post_build_parameters.update(build_result=result)

        if not self.post_build(**pre_and_post_build_parameters):
            print("ERROR: Project post-build hook returned False. Failing the build.")
            result.success = False

        return result

    def open(self, project_path):
        """
        Open the project in Vivado GUI.

        Arguments:
            project_path (`pathlib.Path`): A path containing a Vivado project.

        Returns:
            bool: True if everything went well.
        """
        return run_vivado_gui(self._vivado_path, self.project_file(project_path))

    def _get_size(self, project_path, run):
        """
        Reads the hierarchical utilization report and returns the top level size
        for the specified run.
        """
        report_as_string = read_file(
            project_path / f"{self.name}.runs" / run / "hierarchical_utilization.rpt"
        )
        return UtilizationParser.get_size(report_as_string)

    def __str__(self):
        result = str(self.__class__.__name__)
        if self.defined_at is not None:
            result += f" defined at: {self.defined_at.resolve()}"
        result += "\nName:      " + self.name
        result += "\nTop level: " + self.top
        if self.static_generics is None:
            generics = "-"
        else:
            generics = ", ".join(
                [f"{name}={value}" for name, value in self.static_generics.items()]
            )
        result += "\nGenerics:  " + generics

        return result


class VivadoNetlistProject(VivadoProject):
    """
    Used for handling Vivado build of a module without top level pinning.
    """

    def __init__(self, analyze_clock_interaction=False, result_size_checkers=None, **kwargs):
        """
        Arguments:
            analyze_clock_interaction (bool): Analysis of clock interaction, i.e. checking
                for unhandled clock crossings, is disabled by default. Enabling it will add
                significant build time (can be as much as +40%). Also, in order for clock
                interction check to work, the clocks have to be created using a constraint
                file.
            result_size_checkers (list(:class:`.SizeChecker`)): Size checkers that will be
                executed after a succesful build. Is used to automatically check that
                resource utilization is not greater than expected.
            kwargs: Other arguments accepted by :meth:`.VivadoProject.__init__`.
        """
        super().__init__(**kwargs)

        self.is_netlist_build = True
        self.analyze_clock_interaction = analyze_clock_interaction
        self.result_size_checkers = [] if result_size_checkers is None else result_size_checkers

    def build(self, **kwargs):  # pylint: disable=arguments-differ
        """
        Build the project.

        Arguments:
            kwargs: All arguments as accepted by :meth:`.VivadoProject.build`.
        """
        result = super().build(**kwargs)
        result.success = result.success and self._check_size(result)

        return result

    def _check_size(self, build_result):
        if not build_result.success:
            print(f"Can not do post_build size check for {self.name} since it did not succeed.")
            return False

        success = True
        for result_size_checker in self.result_size_checkers:
            result = result_size_checker.check(build_result.synthesis_size)
            success = success and result

        return success


class BuildResult:

    """
    Attributes:
        project_name (`str`): The name of the build.
        success (`bool`): True if the build and all pre- and post hooks succeeded.
        synthesis_size (`dict`): A dictionary with the utilization of primitives for the
            synthesized design. Will be ``None`` if synthesis failed or did not run.
        implementation_size (`dict`): A dictionary with the utilization of primitives for
            the implemented design. Will be ``None`` if implementation failed or did not run.
    """

    def __init__(self, name):
        """
        Arguments:
            name (`str`): The name of the build.
        """
        self.name = name
        self.success = True
        self.synthesis_size = None
        self.implementation_size = None

    def size_summary(self):
        """
        Return a string with a formatted message of the size.

        Returns:
            str: A human-readable message of the latest size. ``None`` if no size is set.
        """
        build_step = None
        size = None

        if self.implementation_size is not None:
            build_step = "implementation"
            size = self.implementation_size
        elif self.synthesis_size is not None:
            build_step = "synthesis"
            size = self.synthesis_size
        else:
            return None

        return f"Size of {self.name} after {build_step}:\n{json.dumps(size, indent=2)}"
