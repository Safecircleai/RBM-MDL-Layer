"""Era-1 seed: ecosystem operational mandates + consumer registrations.

Per the sprint brief, Era 1 begins with **ecosystem operational mandates** —
deterministic boolean obligations — not government compliance. No trust scoring,
no probabilistic evaluation, no EchoForge consumption.

The seed set (all authored through the real Governance authoring workflow, with
R3 role separation, so nothing is hand-injected into the Registry):

  ecosystem-account-active   PROGRAM · FLOOR   · every node   · account_active
  vbm-deployment-approved    INTERNAL · OVERRIDE · viral-bot-machine    · bot.publish
  prometheus-campaign-approved INTERNAL · OVERRIDE · prometheus         · campaign.activate
  content-media-approved     INTERNAL · OVERRIDE · content-factory      · media.produce
  video-publishing-authorized INTERNAL · OVERRIDE · video-factory       · media.render

Because ``ecosystem-account-active`` sits at PROGRAM (rank 700) and the node
mandates at INTERNAL (rank 800), every determination resolves BOTH — proving the
two-class jurisdiction stack orders a real multi-mandate set, not a single rule.
"""

from __future__ import annotations

from datetime import datetime, timezone

from .domain import (
    Applicability,
    EffectivityWindow,
    InheritanceBehavior,
    JurisdictionLayer,
    Op,
    Rule,
    RuleCategory,
)
from .interface import ConsumerRegistration
from .runtime import MDLRuntime

# Canonical node types (match each consuming repository's identity).
NODE_VBM = "viral-bot-machine"
NODE_PROMETHEUS = "prometheus"
NODE_CONTENT = "safelaunch-content-factory"
NODE_VIDEO = "safelaunch-video-factory"

_OPEN = EffectivityWindow(effective_from="2026-01-01", effective_to=None)


def default_clock() -> str:
    return datetime.now(timezone.utc).isoformat()


def _author_mandate(rt: MDLRuntime, *, intake_id, mandate_id, layer, inheritance, rules, applicability):
    """Run one mandate through Intake→Encode→Review→Approve→Publish.

    Distinct actors for author / reviewer / publisher (R3 separation of duties).
    """
    item = rt.governance.draft(
        intake_id=intake_id,
        source_authority="RBM-Ecosystem-Operations",
        mandate_id=mandate_id,
        jurisdiction_layer=layer,
        inheritance=inheritance,
        rules=rules,
        applicability=applicability,
        effectivity=_OPEN,
        author="gov.author",
    )
    rt.governance.review(item, reviewer="gov.reviewer")
    return rt.governance.publish(item, publisher="gov.publisher")


def seed_mandates(rt: MDLRuntime) -> None:
    _author_mandate(
        rt,
        intake_id="intake-account-active",
        mandate_id="ecosystem-account-active",
        layer=JurisdictionLayer.PROGRAM,
        inheritance=InheritanceBehavior.FLOOR,
        rules=(
            Rule("account.active", RuleCategory.PARTICIPATION, "account_active", Op.IS_TRUE,
                 description="the operating account is active (not suspended/closed)"),
        ),
        applicability=Applicability(),  # every node, every entity — the shared floor
    )
    _author_mandate(
        rt,
        intake_id="intake-vbm-deploy",
        mandate_id="vbm-deployment-approved",
        layer=JurisdictionLayer.INTERNAL,
        inheritance=InheritanceBehavior.OVERRIDE,
        rules=(
            Rule("deploy.operator_authorized", RuleCategory.PARTICIPATION, "operator_authorized", Op.IS_TRUE,
                 description="the requesting operator holds deploy authority"),
            Rule("deploy.intake_approved", RuleCategory.EVIDENCE, "intake_approved", Op.IS_TRUE,
                 description="the bot intake passed the mandatory enhancement review"),
        ),
        applicability=Applicability(
            node_types=(NODE_VBM,), entity_types=("bot_deployment",), purposes=("bot.publish",)
        ),
    )
    _author_mandate(
        rt,
        intake_id="intake-prometheus-campaign",
        mandate_id="prometheus-campaign-approved",
        layer=JurisdictionLayer.INTERNAL,
        inheritance=InheritanceBehavior.OVERRIDE,
        rules=(
            Rule("campaign.governance_passed", RuleCategory.EVIDENCE, "campaign_governance_passed", Op.IS_TRUE,
                 description="the campaign cleared the planning-stage governance validator"),
            Rule("campaign.budget_authorized", RuleCategory.THRESHOLD, "budget_authorized", Op.IS_TRUE,
                 description="the campaign budget is authorized for real (non-simulation) dispatch"),
        ),
        applicability=Applicability(
            node_types=(NODE_PROMETHEUS,), entity_types=("campaign_execution",), purposes=("campaign.activate",)
        ),
    )
    _author_mandate(
        rt,
        intake_id="intake-content-media",
        mandate_id="content-media-approved",
        layer=JurisdictionLayer.INTERNAL,
        inheritance=InheritanceBehavior.OVERRIDE,
        rules=(
            Rule("media.brief_authorized", RuleCategory.EVIDENCE, "brief_authorized", Op.IS_TRUE,
                 description="the media brief is authorized for production"),
        ),
        applicability=Applicability(
            node_types=(NODE_CONTENT,), entity_types=("media_job",), purposes=("media.produce",)
        ),
    )
    _author_mandate(
        rt,
        intake_id="intake-video-publish",
        mandate_id="video-publishing-authorized",
        layer=JurisdictionLayer.INTERNAL,
        inheritance=InheritanceBehavior.OVERRIDE,
        rules=(
            Rule("video.render_authorized", RuleCategory.EVIDENCE, "render_authorized", Op.IS_TRUE,
                 description="the render/voiceover job is authorized to publish media"),
        ),
        applicability=Applicability(
            node_types=(NODE_VIDEO,), entity_types=("render_job",), purposes=("media.render",)
        ),
    )


def register_consumers(rt: MDLRuntime, keys: dict[str, str]) -> None:
    """Register each consuming node with a least-privilege projection.

    ``keys`` maps node_type -> api_key (supplied from the environment). Each node
    may only request determinations for its own node_type, within the Class-2
    operational layers it operates under.
    """
    scope = (JurisdictionLayer.PROGRAM.value, JurisdictionLayer.INTERNAL.value)
    for node_type in (NODE_VBM, NODE_PROMETHEUS, NODE_CONTENT, NODE_VIDEO):
        key = keys.get(node_type)
        if not key:
            continue
        rt.register_consumer(
            ConsumerRegistration(
                node_id=node_type,
                node_type=node_type,
                api_key=key,
                jurisdiction_scope=scope,
                can_determine=True,
                read_only=False,
            )
        )


def build_seeded_runtime(keys: dict[str, str] | None = None, clock=default_clock, now=default_clock) -> MDLRuntime:
    rt = MDLRuntime(clock=clock, now=now)
    seed_mandates(rt)
    register_consumers(rt, keys or {})
    return rt
