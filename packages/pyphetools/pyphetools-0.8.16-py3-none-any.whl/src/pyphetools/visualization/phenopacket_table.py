from collections import defaultdict
from typing import Dict, List
from functools import cmp_to_key
import sys

from ..creation.constants import Constants
from ..creation.hp_term import HpTerm
from .simple_patient import SimplePatient
from .html_table_generator import HtmlTableGenerator


#


class Age2Day:
    """
    Convenience function to help sort ages but converting ISO8601 strings into the number of days

        sorted_age = sorted(l, key=lambda x: x.days)

    following this, retrieve the original string as x.key
    """
    def __init__(self, age) -> None:
        self.key = age
        if age == Constants.NOT_PROVIDED:
            self.days = sys.maxsize
        elif not age.startswith("P"):
            raise ValueError(f"Invlaid age string: {age}")
        else:
            days = 0
            age = age[1:]
            N = len(age)
            y = age.find("Y")
            if y != -1:
                days = days + 365*int(age[:y])
                age = age[y+1:]
            m = age.find("M")
            if m != -1:
                days = days + 30.436875*int(age[:m])
                age = age[m+1:]
            d = age.find("D")
            if d != -1:
                days = days + int(age)
            self.days = days








class PhenopacketTable:
    """
    This class creates a table with a summary of all phenopackets in a cohort of individuals
    Create Individual objects and transform them into phenopackets, or import GA4GH phenopackets and display them.

        from IPython.display import HTML, display
        phenopackets = [i.to_ga4gh_phenopacket(metadata=metadata) for i in individuals]
        table = PhenopacketTable(phenopacket_list=phenopackets)
        display(HTML(table.to_html()))
    """
    def __init__(self, phenopacket_list) -> None:
        """
        :param phenopacket_list: List of GA4GH phenopackets to be displayed
        """
        if not isinstance(phenopacket_list, list):
            raise ValueError(f"Expecting a list but got {type(phenopacket_list)}")
        if len(phenopacket_list) == 0:
            raise ValueError("phenopacket_list was empty")
        ppkt = phenopacket_list[0]
        if str(type(ppkt)) != "<class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>":
            raise ValueError(f"phenopacket argument must be GA4GH Phenopacket Schema Phenopacket but was {type(ppkt)}")
        self._phenopacket_list = phenopacket_list

    def _phenopacket_to_table_row(self, spat) -> List[str]:
        """
        private method intended to create one table row that represents one individual
        :param spat: An object that represents one individual
        :type spat: SimplePatient
        """
        row_items = []
        # Patient information
        pat_info = spat.get_subject_id() + " (" + spat.get_sex() + "; " + spat.get_age() + ")"
        row_items.append( pat_info)
        row_items.append( spat.get_disease())
        # Variant information
        var_list = spat.get_variant_list()
        if len(var_list) == 0:
            row_items.append("n/a" )
        elif len(var_list) == 1:
            var = var_list[0]
            row_items.append( var.get_display() )
        else:
            cell_items = []
            cell_items.append("<ul>")
            for var in var_list:
                cell_items.append("<li>" + var.get_display() + "</li>")
            cell_items.append("</ul>")
            row_items.append( " ".join(cell_items) )
        # HPO information
        hpo_html = self.get_hpo_cell(spat.get_term_by_age_dict())
        row_items.append( hpo_html )
        return row_items


    def get_hpo_cell(self, term_by_age_dict:Dict[str,HpTerm]) -> str:
        """
        :param term_by_age_dict: A dictionary with key - ISO8601 string, value - list of HpTerm objects
        :type term_by_age_dict: Dict[str,HpTerm]
        :returns: HTML code for the HTML cell
        :rtype: str
        """
        lines = []
        age2day_list = list(Age2Day(x) for x in term_by_age_dict.keys())
        sorted_age = sorted(age2day_list, key=lambda x: x.days)
        for onset in sorted_age:
            hpo_list = term_by_age_dict.get(onset.key)
            hpos = "; ".join([hpo.__str__() for hpo in hpo_list])
            if onset.key == Constants.NOT_PROVIDED:
                lines.append(hpos)
            else:
                lines.append(f"<b>{onset.key}</b>: {hpos}")
        return "<br/>".join(lines)

    def to_html(self):
        """create an HTML table with patient ID, age, sex, genotypes, and PhenotypicFeatures
        """
        ppack_list = self._phenopacket_list
        spat_list = []
        pmid_count_d = defaultdict(int)
        no_pmid_found = 0
        pmid_found = 0
        for pp in ppack_list:
            spat = SimplePatient(ga4gh_phenopacket=pp)
            if spat.has_pmid():
                pmid_count_d[spat.get_pmid()] += 1
                pmid_found += 1
            else:
                no_pmid_found += 1
            spat_list.append(spat)
        # Create caption
        if pmid_found == 0:
            capt = f"{len(ppack_list)} phenopackets - no PMIDs (consider adding this information to the MetaData)"
        else:
            pmid_strings = []
            for k, v in pmid_count_d.items():
                pmid_strings.append(f"{k} (n={v})")
            pmid_str = "; ".join(pmid_strings)
            capt = f"{len(ppack_list)} phenopackets - {pmid_str}"
        header_items = ["Individual", "Disease", "Genotype", "Phenotypic features"]
        rows = []
        for spat in spat_list:
            rows.append(self._phenopacket_to_table_row(spat))
        generator = HtmlTableGenerator(caption=capt, header_items=header_items, rows=rows)
        return generator.get_html()

