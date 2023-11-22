# Contributing to Nyx

First off, thanks for considering contributing Nyx! :tada::+1:

Your knowledge of software and astrodynamics is what will help developing an active community around this project.

A core principle exists for all of the following document: as this code is open-source and available to the public, never mention the name of a customer in _any_ commit message unless you sought and received the customer's direct approval.

## Reporting issues

If you have found a bug in the toolkit, please report an issue explaining what was the expected result and what Nyx returned instead. It is very important that Nyx is bug free and thoroughly validated.

If possible, please provide a simple example of how to reproduce the bug in the form of a function (e.g. `main` with the correct imports). This will ensure that the bug can be reproduced and therefore fixed accordingly.
If this is a validation issue, please provide a reference to a paper or another high-fidelity simulation tool which confirms that the result returned by Nyx is incorrect.

## Helping out with development

There is a lot to do before this toolkit can even start to gain any adoption! Any help is appreciated.

Check out the list of issues, and eventually the milestones.
The milestones exist as a non-exhaustive list of what is expected from each tagged version.

If you plan on opening a pull request for some code changes, first ensure that an issue exists for those changes. If not, create one, and assign yourself (or mention that you'll work on it in the body).
Then, for traceability purposes, please create a branch which contains the issue number (best is to see the branch name recommended by Github).

Finally, also for traceability, please try to sign at least the final commit of the code changes with your GPG key.

### Guidelines

All the guidelines for software development and testing can be found on <https://quality.nyxspace.com>. This is a living document that is meant to be copied and used by others, so don't hesitate to copy and modify it for use in your own projects, personal or corporatte.

### Validation of changes
If the proposed changes are related to the dynamics or the propagation models, please include both a relevant test case and a relevant GMAT script for future reference, and detail which version of GMAT was used to validate this result (e.g. `2017a`).

The test will be automatically executed in the Github CI.

### Self-review
You may do a self-review of your code if you have writing privileges on the repo. If so, it is recommended to push the code, check that the test succeed and then take a break for _a few hours_! After that, come back and objectively review your code.
It's OK to notice that you could have done things better in the first place. Finally, one recommendation is to run [`cargo clippy`](https://github.com/rust-lang/rust-clippy) on the code to see if your additions could be coded up more simply.
