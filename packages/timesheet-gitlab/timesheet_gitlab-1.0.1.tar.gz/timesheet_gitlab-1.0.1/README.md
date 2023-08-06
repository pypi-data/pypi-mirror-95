# timesheet_gitlab

Produces timesheets using activity data from GitLab API calls.

The project arose from a need to submit daily timesheets and a monthly
summary for a client. 
The way I prefer to code involves using an issue page for each separate 
development, then making frequent comments
about each part of the work together with numerous commits/pushes. Each of
these contributions already produces a timestamped record that can be viewed 
at my activity page https://gitlab.com/oliversmart. The 
tool `timesheet_gitlab` accesses the 
relevant data from the GitLab.com API. It then processes the records 
into 30-minute bins, and a daily/monthly timesheets are 
produced using these. 
The PDF timesheet includes hyperlinks to particular issue comments that can
be accessed in a web browser (by authorized accounts) and so there is
a high degree of traceability.

Please note that this way of producing timesheets 
suits my way of working (I try to use 
[Pomodoro Technique](https://francescocirillo.com/pages/pomodoro-technique)).
For many people it would be too intrusive as it involves making
a comment or code push every 30-minutes (although there is a way to mark a slot
if you forget - see below). I would certainly strongly advise against
imposing this method on anyone else.

An alternative lightweight approach is GitLab.com Time-Tracking
https://about.gitlab.com/solutions/time-tracking/. Project 
[gitlab-cli-reports](https://gitlab.com/incomprehensibleaesthetics/gitlab-cli-reports)
looks like a good way to produce timesheets from time-tracking information.

`timesheet_gitlab` uses 
[python-gitlab](https://python-gitlab.readthedocs.io/en/latest/index.html)
to make the GitLab API calls.  The timesheet is written as markdown
that can then be viewed in a web browser using 
[grip](https://github.com/joeyespo/grip).

If anyone else finds `timesheet_gitlab` useful please let me know. Please feel free to
raise any suggestions or problems using issues. Currently,
all times are [UTC](https://www.wikiwand.com/en/Coordinated_Universal_Time)
that matches the local time here in England in the winter.

## Installation

_Should be via pip in the end._

To use the tool you will need a private personal access token to 
authenticate with the GitLab API. For instructions, please see 
https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html

## Example run A: today's timesheet

By default, timesheet_gitlab will write the timesheet for today 
in markdown. To save this to a file use redirection:
<pre>
$ <b>timesheet_gitlab > today.md</b>
</pre>
The markdown file can then be viewed using the grip tool:
<pre>
$ <b>grip -b today.md</b>
</pre>
Or to avoid writing a file a pipe can be used:

<pre>
$ <b>timesheet_gitlab | grip -b -</b>
</pre>


At the time of writing this produced a timesheet, showing the work done
on this `timesheet_gitlab` project:

> ### Daily time sheet for Saturday 20 Feb 2021
>
> >  | **time slot** | **activities** |
> >  | ----------------- | -------------- |
> >  | 08:30&#8209;08:59  | [`timesheet_gitlab: commented on issue #3`](https://GitLab.com/oliversmart/timesheet_gitlab/-/issues/3#note_513507083) |
> >  | 10:00&#8209;10:29  | `timesheet_gitlab: pushed commit(s)`, [`timesheet_gitlab: commented on issue #3`](https://GitLab.com/oliversmart/timesheet_gitlab/-/issues/3#note_513519860) |
> >  | 11:00&#8209;11:29  | `timesheet_gitlab: pushed commit(s)` |
> >  | 11:30&#8209;11:59  | `timesheet_gitlab: pushed commit(s)`, [`timesheet_gitlab: commented on issue #3`](https://GitLab.com/oliversmart/timesheet_gitlab/-/issues/3#note_513534178) |
> >  | 16:00&#8209;16:29  | [`timesheet_gitlab: commented on issue #3`](https://GitLab.com/oliversmart/timesheet_gitlab/-/issues/3#note_513608749), `timesheet_gitlab: pushed commit(s)` |
> > 
> > **Hours worked: 2.5**

Note that the hyperlinks are to the particular comment(s) in the issue 
made at that time.

## Example run B: Monthly timesheet for this project.

To produce a monthly timesheet for this project use the --filter option for
this project name. To produce a monthly timesheet specify the start date
as 1 for the first of February to the 28th February:

<pre>
$ <b>timesheet_gitlab --filter timesheet_gitlab 1-2 28-2 > timesheet_project_feb_2020.md</b>
</pre>

This produces a markdown file: 
[timesheet_project_feb_2020.md](example_output/timesheet_project_feb_2020.md)
The `grip` tool can be used to view the file locally and save a PDF file
for submission. In this case, the timesheet shows that this project
took just over 3 working days to get to public release.

## How to manually add a missed timeslot

Say you were in a meeting from 10am to 12noon but had only recorded
notes afterwards in an issue. Add a comment like:
```

Meeting about ****** from 10am to noon.
* general discuss about *****

<!-- TSADD_10:00_TADD TSADD_10:30_TSADD 
     TSADD_11:00_TADD TSADD_11:30_TSADD -->
```
The html comment will add activities in the 10:00, 10:30, 11:00 and 11:30
slots to `timesheet_gitlab` but not be visible on the issue page.