from leapp import reporting
from leapp.actors import Actor
from leapp.models import TargetRepositories, UsedTargetRepositories
from leapp.reporting import Report
from leapp.tags import IPUWorkflowTag, TargetTransactionChecksPhaseTag


class LocalReposInhibit(Actor):
    """Inhibits the upgrade if local repositories were found.

    Currently we're not supporting local repositories during the upgrade.
    There is a workaround available, which described inside the remediation of
    the report.

    We're looking for a baseurl only inside TargetRepositories.custom_repos
    because local repos might exists as only custom repository, due to the
    fact that they might be specified only inside custom repo file of the leapp
    or via --enablerepo flag. Both options puts the repo into
    CustomTargetRepository.
    """

    name = "local_repos_inhibit"
    consumes = (UsedTargetRepositories, TargetRepositories)
    produces = (Report,)
    tags = (IPUWorkflowTag, TargetTransactionChecksPhaseTag)

    def get_used_custom_repos(self):
        """Get used custom repositories.

        :returns: Generator[CustomTargetRepository]
        """
        # fmt: off
        used_target_repos = next(self.consume(UsedTargetRepositories)).repos
        custom_target_repos = next(self.consume(TargetRepositories)).custom_repos
        # fmt: on
        used_target_repos_ids = [
            used_tg_repo.repoid for used_tg_repo in used_target_repos
        ]
        return filter(  # pylint: disable-msg=deprecated-lambda, filter-builtin-not-iterating
            lambda custom_target_repo: custom_target_repo.repoid
            in used_target_repos_ids
            and custom_target_repo.baseurl,
            custom_target_repos,
        )

    def process(self):
        for custom_repo in self.get_used_custom_repos():
            if custom_repo.baseurl.startswith("file:"):
                self.log.warning(
                    "Local repository %r found. Referring to baseurl: %s. "
                    "Currently leapp not supporting this option",
                    custom_repo.repoid,
                    custom_repo.baseurl,
                )
                reporting.create_report(
                    [
                        reporting.Title("Local repository identified"),
                        reporting.Summary(
                            (
                                "Local repository {} with baseurl {} found. "
                                "Currently leapp does not support this option."
                            ).format(custom_repo.repoid, custom_repo.baseurl)
                        ),
                        reporting.Severity(reporting.Severity.HIGH),
                        reporting.Tags([reporting.Tags.REPOSITORY]),
                        reporting.Flags([reporting.Flags.INHIBITOR]),
                        reporting.Remediation(
                            hint=(
                                "By using Apache HTTP Server you can expose "
                                "your local repository via http. For details "
                                "see external link."
                            )
                        ),
                        reporting.ExternalLink(
                            title=(
                                "Customizing your Red Hat Enterprise Linux "
                                "in-place upgrade"
                            ),
                            url=(
                                "https://access.redhat.com/articles/4977891/"
                                "#repos-known-issues"
                            ),
                        ),
                    ]
                )
                break
