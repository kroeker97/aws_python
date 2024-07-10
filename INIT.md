1. Copy template to new git repository
    - checkout new git repository
    - download [tcs-node-libraries](https://bitbucket.org/tecracer/tcs-node-libraries/src/main/) as zip
    ![img](./docs/workflows/bitbucket-download-template.png)
    - extract the content of the zipped folder to the new checked out git repository
2. Replace all (where `project` is an abbreviation of your new project):
    - `@template/` -> `@project/` (local packages)
    - `tcs-template-` -> `project-` (Bitbucket pipelines resource naming, if used)
3. edit the following sections in the [README.md](./README.md) file to match your project decisions
    - `Branching`
    - `Deployment`
    - `Architecture of applications`
4. edit [bitbucket-pipelines.yml](./bitbucket-pipelines.yml) (if needed)
5. stage all changes via `git add --all`
6. commit `git commit -m "chore: init #[YOUR-JIRA-ISSUE]"`
7. `git push`
