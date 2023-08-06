"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import argparse

from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cli.utils import get_outfile
from pmidcite.cli.utils import get_pmids
from pmidcite.icite.nih_grouper import NihGrouper


class NIHiCiteCli:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self, pmidcite):
        self.pmidcite = pmidcite
        cfgparser = self.pmidcite.cfgparser
        self.pubmed = PubMed(
            email=cfgparser.get_email(),
            apikey=cfgparser.get_apikey(),
            tool=cfgparser.get_tool())

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        dir_icite_py = self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_icite_py']
        dir_icite = self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_icite']
        dir_pubmed_txt = self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_pubmed_txt']
        parser.add_argument(
            'pmids', metavar='PMID', type=int, nargs='*',
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '-i', '--infile', nargs='*',
            help='Read PMIDs from a file containing one PMID per line.')
        parser.add_argument(
            '-a', '--append_outfile',
            help='Append current citation report to an ASCII text file. Create if needed.')
        parser.add_argument(
            '-H', '--print_header', action='store_true',
            help='Print column headings on one line.')
        parser.add_argument(
            '-k', '--print_keys', action='store_true',
            help='Print the keys describing the abbreviations.')
        parser.add_argument(
            '-o', '--outfile',
            help='Write current citation report to an ASCII text file.')
        parser.add_argument(
            '-O', action='store_true',
            help="Write each PMIDs' iCite report to <dir_icite>/PMID.txt")
        parser.add_argument(
            '-f', '--force_write', action='store_true',
            help='if an existing outfile file exists, overwrite it.')
        parser.add_argument(
            '-D', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file, over-writing if necessary.')
        parser.add_argument(
            '--dir_icite_py', default=dir_icite_py,
            help='Write PMID iCite information into directory (default={D})'.format(D=dir_icite_py))
        parser.add_argument(
            '--dir_icite', default=dir_icite,
            help='Write PMID icite reports into directory (default={D})'.format(D=dir_icite))
        parser.add_argument(
            '-R', '--no_references', action='store_true',
            help='Print the list of citations, but not the list of references.')
        parser.add_argument(
            '-v', '--verbose', action='store_true', default=False,
            help="Print all citing papers and references for each PMID provided by user.")
        parser.add_argument(
            '-p', '--pubmed', action='store_true',
            help='Download PubMed entry containing title, abstract, authors, journal, MeSH, etc.')
        parser.add_argument(
            '--dir_pubmed_txt', default=dir_pubmed_txt,
            help='Write PubMed entry into directory (default={D})'.format(D=dir_pubmed_txt))
        self.pmidcite.cfgparser.get_nihgrouper().add_arguments(parser)
        parser.add_argument(
            '--md', action='store_true',
            help='Print using markdown table format.')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        ## print('ICITE ARGS', args)
        self.pmidcite.dir_icite_py = args.dir_icite_py
        groupobj = NihGrouper(args.min1, args.min2, args.min3, args.min4)
        dnldr = self.get_icite_downloader(groupobj, args.force_download, args.no_references)
        pmids = get_pmids(args.pmids, args.infile)
        pmid2icitepaper = dnldr.get_pmid2paper(pmids, not args.no_references, None)
        self.run_icite(pmid2icitepaper, dnldr, args, argparser)
        # pylint:disable=line-too-long
        if args.pubmed:
            self.pubmed.dnld_wr1_per_pmid(pmids, args.force_download, args.dir_pubmed_txt)

    # pylint: disable=too-many-arguments
    def run_icite(self, pmid2icitepaper_all, dnldr, args, argparser):
        """Run iCite/PubMed"""
        pmid2icitepaper_cur = self.run_icite_pre(pmid2icitepaper_all, dnldr, args, argparser)
        if not pmid2icitepaper_cur:
            return
        if args.O:
            self._wr_papers(pmid2icitepaper_cur, dnldr)
        else:
            self.run_icite_wr(pmid2icitepaper_cur, args, dnldr)

    def run_icite_pre(self, pmid2icitepaper_all, dnldr, args, argparser):
        """Run iCite/PubMed"""
        ## print('ICITE ARGS: ../pmidcite/src/pmidcite/cli/icite.py', args)
        # Print rcfile initialization file
        if args.generate_rcfile:
            self.pmidcite.prt_rcfile(sys.stdout)
            return {}
        # Get user-specified PMIDs
        if not pmid2icitepaper_all and not args.print_keys and not args.print_header:
            argparser.print_help()
            self._prt_infiles(args.infile)
        if args.print_keys:
            dnldr.prt_keys()
        if args.print_header:
            dnldr.prt_hdr()
        pmid2icitepaper_cur = {p: o for p, o in pmid2icitepaper_all.items() if o is not None}
        if not pmid2icitepaper_cur:
            # pylint: disable=line-too-long
            self._prt_no_icite(set(pmid2icitepaper_all.keys()).difference(pmid2icitepaper_cur.keys()))
            return {}
        return pmid2icitepaper_cur

    @staticmethod
    def _prt_infiles(infiles):
        """Print input files"""
        if infiles:
            for fin in infiles:
                print('**ERROR: NO PMIDs found in: {F}'.format(F=fin))

    @staticmethod
    def run_icite_wr(pmid2icitepaper, args, dnldr):
        """Print papers, including citation counts"""
        dct = get_outfile(args.outfile, args.append_outfile, args.force_write)
        prt_verbose = args.verbose
        if dct['outfile'] is None and not args.O:
            dnldr.prt_papers(
                pmid2icitepaper, prt=sys.stdout, prt_assc_pmids=prt_verbose)
        else:
            if args.verbose:
                dnldr.prt_papers(pmid2icitepaper, prt=sys.stdout, prt_assc_pmids=prt_verbose)
            if dct['outfile'] is not None:
                dnldr.wr_papers(dct['outfile'], pmid2icitepaper, dct['force_write'], dct['mode'])

    def _wr_papers(self, pmid2icitepaper, dnldr):
        """Write one icite report per PMID into dir_icite/PMID.txt"""
        for pmid, paper in pmid2icitepaper.items():
            fout_txt = os.path.join(self.pmidcite.dir_icite, '{PMID}.txt'.format(PMID=pmid))
            with open(fout_txt, 'w') as prt:
                dnldr.prt_papers({pmid:paper}, prt, prt_assc_pmids=True)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))

    @staticmethod
    def _prt_no_icite(pmids):
        if not pmids:
            return
        print('**NOTE: No NIH iCite papers found for: {Ps}'.format(
            Ps=' '.join(str(p) for p in pmids)))

    def get_icite_downloader(self, grouperobj, force_download, no_references):
        """Get iCite downloader"""
        # pylint: disable=line-too-long
        return self.pmidcite.get_icitedownloader(force_download, grouperobj, no_references, prt_icitepy=None)

    #def _get_pmid2icitepaper(self, pmids, grouperobj, args):
    #    """Get pmid2icitepaper"""
    #    dnldr = self.pmidcite.get_icitedownloader(args.force_download, grouperobj, args.no_references, prt=None)
    #    if args.print_keys:
    #        dnldr.prt_keys()
    #    dct = get_outfile(args.outfile, args.append_outfile, args.force_write)
    #    prt_verbose = not args.succinct
    #    return dnldr.get_pmid2paper(pmids, not args.no_references, pmid2note)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
