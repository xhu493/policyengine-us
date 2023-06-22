from policyengine_us.model_api import *


class pa_tanf_unearned_income(Variable):
    value_type = float
    entity = SPMUnit
    label = "PA TANF unearned income"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.PA

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.pa.dhs.tanf.income

        # Sum unearned sources, plus child support disregard $150 received per month.
        gross_unearned = add(spm_unit, period, p.unearned)
        child_support = add(spm_unit, period, ["child_support_received"])
        monthly_child_support_deduction = (
            p.unearned_deduction.monthly_child_support
        )
        child_support_after_deduction = max_(
            child_support - monthly_child_support_deduction * MONTHS_IN_YEAR, 0
        )
        return gross_unearned + child_support_after_deduction