from openfisca_us.model_api import *


class state_income_tax_rental_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "State income tax rental deduction"
    unit = USD
    documentation = "State income tax rental deduction"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        rent = tax_unit.spm_unit("rent", period)
        p = parameters(period).states.tax.income.deductions.rent
        state = tax_unit.household("state_code_str", period)
        mars = tax_unit("marital_status", period)
        share = p.share[state]
        cap = p.cap[state][mars]
        uncapped = rent * share
        return min_(uncapped, cap)
