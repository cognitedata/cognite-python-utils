Recommended Practices
=====================

Run Pre-Commit Hooks
--------------------

Consistent coding standards enable effective code review and maintenance. Hence, we strongly recommend
you use pre-commit hooks set for the project. You can install them by running:

.. code:: bash

    $ pre-commit install

Then, whenever you are about to make a new commit, run:

.. code:: bash

    $ pre-commit run --all-files

to automatically apply coding standards set for the project.

Organize Each PR with Relevant Changes
--------------------------------------

To maintain a linear/cleaner project history, the project was set up to apply “squashing” when merging a PR.
That is, if a PR contains more than one commit, GitHub will combine them into a single commit where the summary
equals the PR title (followed by the PR number) and the description consists of commit messages for all squashed
commits (in date order). Hence, we ask you to organize each PR with related changes only so that it can represent
a single unit of meaningful change.
