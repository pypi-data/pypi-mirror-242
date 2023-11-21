"""A Vulnerability Scanner that combines results from all configured scanners."""
# This file is part of hoppr-cop
#
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Copyright (c) 2022 Lockheed Martin Corporation
from __future__ import annotations

import concurrent.futures
import importlib

from typing import TYPE_CHECKING

import typer

from hoppr_security_commons.vulnerability_combiner import combine_vulnerabilities
from hoppr_security_commons.vulnerability_scanner import VulnerabilitySuper
from rich.progress import Progress, SpinnerColumn, TextColumn


if TYPE_CHECKING:
    from hoppr_cyclonedx_models.cyclonedx_1_3 import (
        CyclonedxSoftwareBillOfMaterialSpecification as Bom_1_3,
    )
    from hoppr_cyclonedx_models.cyclonedx_1_4 import (
        CyclonedxSoftwareBillOfMaterialsStandard as Bom_1_4,
        Vulnerability,
    )
    from packageurl import PackageURL


class CombinedScanner(VulnerabilitySuper):
    """A Vulnerability Scanner that combines results from all configured scanners."""

    scanners: list[VulnerabilitySuper] = []

    def set_scanners(self, scanners: list[VulnerabilitySuper] | list[str]):
        """Sets the scanners that should be used for vulnerability scanning.
        The argument can either be a list of scanner instances or a list of fully qualified strings to a scanner
         instance. For example ["vuln.gemnasium.gemnasium_scanner.GemnasiumScanner"].
        """
        for scanner in scanners:
            if isinstance(scanner, str):
                modname, _, clsname = scanner.rpartition(".")
                mod = importlib.import_module(modname)
                scanner = getattr(mod, clsname)()

            if scanner.should_activate():
                typer.echo(f"{scanner.__class__.__name__} is activated")
                self.scanners.append(scanner)

    def ___scan_concurrently(self, function) -> dict[str, list[Vulnerability] | None]:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            results = []
            progress.add_task(description="Fetching vulnerabilities...", total=None)
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                futures = {executor.submit(function, scanner): scanner for scanner in self.scanners}
            for future in concurrent.futures.as_completed(futures):
                scanner = futures[future]
                try:
                    scanner_results = future.result()
                    results.append(scanner_results)
                    # if not found:
                    #     failed.append(purl)
                except Exception as exc:
                    print(f"{scanner.__class__.__name__} generated an exception: {exc}")
        return combine_vulnerabilities(list(results))

    def get_vulnerabilities_by_purl(self, purls: list[PackageURL]) -> dict[str, list[Vulnerability] | None]:
        """Get the vulnerabilities for a list of package URLS (purls)
        This function will return a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """

        def submit_to_scanner_purl(scanner: VulnerabilitySuper):
            return scanner.get_vulnerabilities_by_purl(purls)

        return self.___scan_concurrently(submit_to_scanner_purl)

    def get_vulnerabilities_by_sbom(self, bom: [Bom_1_4 | Bom_1_3]) -> dict[str, list[Vulnerability] | None]:
        """Parse a cyclone dx 1.4 compatible BOM and return a list of vulnerabilities "
        This function will return a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """

        def submit_to_scanner(scanner: VulnerabilitySuper):
            return scanner.get_vulnerabilities_by_sbom(bom)

        return self.___scan_concurrently(submit_to_scanner)
