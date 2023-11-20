##############################################################################
# Copyright (C) 2020 - 2023 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of f4ratk.
#
# f4ratk is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from flask import Blueprint, Response, make_response, request
from marshmallow import EXCLUDE, Schema, post_load
from marshmallow.fields import Float, Integer, Nested
from marshmallow.validate import Range

from f4ratk.cost import Accountant, Statements
from f4ratk.infrastructure import di

cost_blueprint = Blueprint(name='cost', import_name=__name__)


class CostBreakdownRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    totalExpenseRatio = Float(required=True, validate=Range(min=0, min_inclusive=False))
    expenses = Integer(required=True)
    transactionCosts = Integer()
    withholdingTax = Integer()
    capitalGainsTax = Integer()
    securitiesLendingIncome = Integer()

    @post_load
    def to_statements(self, data: dict, **_):
        return Statements(
            total_expense_ratio=data.get('totalExpenseRatio'),
            expenses=data.get('expenses'),
            transaction_costs=data.get('transactionCosts'),
            withholding_tax=data.get('withholdingTax'),
            capital_gains_tax=data.get('capitalGainsTax'),
            securities_lending_income=data.get('securitiesLendingIncome'),
        )


class CostIncreasesSchema(Schema):
    total_expense_ratio = Float(data_key='totalExpenseRatio', required=True)
    withholding_tax_ratio = Float(data_key='withholdingTaxRatio')
    capital_gains_tax_ratio = Float(data_key='capitalGainsTaxRatio')
    transaction_costs_ratio = Float(data_key='transactionCostsRatio')


class CostDecreasesSchema(Schema):
    securities_lending_ratio = Float(data_key='securitiesLendingRatio')


class CostBreakdownSchema(Schema):
    increases = Nested(CostIncreasesSchema)
    decreases = Nested(CostDecreasesSchema)
    total_costs_ratio = Float(data_key='totalCostsRatio')


@cost_blueprint.route('/v0/costs', methods=['POST'])
def costs() -> Response:
    statements: Statements = CostBreakdownRequestSchema().load(request.get_json())

    cost_breakdown = di[Accountant].assess(statements)

    return make_response(CostBreakdownSchema().dump(cost_breakdown))
