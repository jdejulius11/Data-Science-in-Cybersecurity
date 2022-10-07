===========================================================
Routeviews Prefix-to-AS mappings (pfx2as) for IPv4 and IPv6
===========================================================


* Overview

This Dataset contains IPv4/IPv6 Prefix-to-Autonomous System (AS) mappings
derived from RouteViews data (http://www.routeviews.org).


---------------------------------------------------------------------------
* Creation Process

Files are generated with straightenRV using a single BGP table
snapshot (that is, a RIB file) provided by RouteViews.

In order to avoid truncated or otherwise problematic BGP snapshots,
we choose the median-sized BGP snapshot file from all the snapshots
available on a given day.

For IPv4, we've used two different collectors over time, oix and rv2:

  - The pfx2as files with "oix" in the name were generated from
    route-views.routeviews.org (aka route-views.oregon-ix.net) snapshots.
    The "oix" collector is one of the oldest RouteViews collectors, and it
    had the most peers until its deactivation in late Mar 2008.

  - The pfx2as files with "rv2" in the name were generated from
    route-views2.routeviews.org snapshots. We switched over to "rv2" in
    late Mar 2008.  The "rv2" collector has a slightly different set of
    peers than "oix", but for prefix-to-AS mapping, the two collectors
    should be comparable.

For IPv6, we use rv6 (route-views6) collector.


---------------------------------------------------------------------------
* New File Creation Log

We have tried to make it easy for you to set up an automated process to
download new pfx2as files as they are produced.  The best way to do this is
to download the file pfx2as-creation.log once a day.  Whenever we provide a
new file for download, we add a new line to this log file.  Simply download
and examine this log file to discover which new files have been added since
your last batch of downloads.  See the comments in the log file for further
details.

  NOTE: There are two separate log files, one for IPv4 at

http://data.caida.org/datasets/routing/routeviews-prefix2as/pfx2as-creation.log

        and one for IPv6 at

http://data.caida.org/datasets/routing/routeviews6-prefix2as/pfx2as-creation.log


---------------------------------------------------------------------------
* File Naming

The file naming convention is

  routeviews-<peer>-<snapshot-date-and-time>.pfx2as.gz

For example, a pfx2as file generated from an rv2 snapshot taken on
20080401-0907 would be named

  routeviews-rv2-20080401-0907.pfx2as.gz

The snapshot time is in UTC.


---------------------------------------------------------------------------
* Data Format

Once unpacked (with gunzip or gzip -d for example), these files can be used
directly with CAIDA's ASFinder and various CoralReef tools (such as the
t2_convert -R option).  For more information about these tools see
http://www.caida.org/tools/measurement/coralreef/

The file format is line-oriented, with one prefix-AS mapping per line.  The
tab-separated fields are

   * IP prefix
   * prefix length
   * AS

The AS can be a single AS number, an AS set (e.g. {32,54} ), or a multi-origin 
AS (e.g. 10_20 ).

From the documentation of AS links files 
(http://www.caida.org/data/active/ipv4_routed_topology_aslinks_dataset.xml), 
which use pfx2as files for mapping to ASes:

In all places where an AS number can appear in this file format, there can
also be an AS set or a multi-origin AS (MOAS).  An AS set is a valid
component of BGP AS paths.  They are usually printed as a list of
comma-separated AS numbers enclosed in curly braces; for example, {32,54}.
In this file format, AS sets are printed without the curly braces: 32,54.
AS sets will never have spaces around the comma separator.

A multi-origin AS occurs when a given BGP prefix is announced by more than
one AS.  Suppose some prefix 10.0.0.0/8 is announced in the BGP table by
both AS 10 and AS 20.  Then an address in that prefix, like 10.0.0.1, will
map to both AS 10 and AS 20.  This is indicated by using the pseudo AS
number 10_20.  If AS 30 also announces that prefix, then you would see
10_20_30.  If the AS set {32,54} also announces the prefix, then you would
see 10_20_30_32,54 where the grouping is AS 10, AS 20, AS 30, and the AS
set {32,54}.

  =========================================================================
  NOTE: The file format changed slightly beginning with the 2010-10-27
        prefix-to-AS file.  Previously, ASes were listed in sorted
        order in MOASes (for example, we said "10_20_30" and never
        "30_10_20").  Now, we sort the ASes according to their
        frequency of appearance as an origin AS in the source BGP
        table.  For example, suppose 10.0.0.0/8 is advertised by the
        ASes 10, 20, and 30, and suppose 7 RouteViews peers saw AS 10
        as the origin AS, 4 saw AS 20 as the origin AS, and 29 saw AS
        30 as the origin AS.  Then the MOAS recorded in the
        prefix-to-AS file will be 30_10_20, according to descending
        frequency of appearance as an origin AS.  If there is a tie in
        frequency, then we sort by lexicographical order.  With the
        new sorting order, users who wish to choose "the best" mapping
        for simplicity (with full understanding of the caveats) can
        simply pick the first listed AS.
  =========================================================================

# $Header: /cvs/Production/datasets/pfx2as/README,v 1.6 2013/04/16 00:56:13 youngh Exp $
