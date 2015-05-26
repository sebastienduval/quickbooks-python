import json
import datetime
import pytz


class BaseBuilder(object):

    def __init__(self):
        self.request = {}

    def to_json(self):
        return json.dumps(self.request)

    def sanitize_length(self, var_name, value, length):
        if len(value) > length:
            raise error(var_name + ' has a maximum length of ' + length + ' characters.')

    def sanitize_from_set(self, var_name, value, value_set):
        if value not in value_set:
            raise error(var_name + '(' + value + ') is not part of ' + value_set)

    def sanitize_boolean(self, var_name, value):
        if not isinstance(value, bool):
            raise error(var_name + ' is a boolean value.')

    @staticmethod
    def convert_date(date):
        """Converts a datetime object into a UTC QBOL compatible string date."""
        if date.tzinfo is None:
            utcdate = pytz.UTC.localize(date)
        else:
            utcdate = date.astimezone(pytz.UTC)
        # Save to the appropriate format.
        return utcdate.strftime('%Y-%m-%dZ')


class AccountRequestBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def active(self, value):
        self.sanitize_boolean('Active', value)
        self.request['Active'] = value
        return self

    def fully_qualified_name(self, value):
        self.request['FullyQualifiedName'] = value
        return self

    def name(self, value):
        self.request['Name'] = value
        return self

    def description(self, value):
        self.request['Description'] = value
        return self

    def account_type_bank(self):
        self.__set_account_type('Bank')
        return self

    def account_type_expense(self):
        self.__set_account_type('Expense')
        return self

    def account_type_receivable(self):
        self.__set_account_type('Accounts Receivable')
        return self

    def __set_account_type(self, value):
        self.request['AccountType'] = value

    def account_sub_type_receivable(self):
        self.__set_account_sub_type('AccountsReceivable')
        return self

    def account_sub_type_service_fee_income(self):
        self.__set_account_sub_type('ServiceFeeIncome')
        return self

    def __set_account_sub_type(self, value):
        self.request['AccountSubType'] = value


class CustomerRequestBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def active(self, value):
        self.request['Active'] = value
        return self

    def billing_address(self, physical_address_builder):
        self.request['BillAddr'] = physical_address_builder.request
        return self

    def company_name(self, value):
        self.sanitize_length('CompanyName', value, 50)
        self.request['CompanyName'] = value
        return self

    def default_tax_code_ref(self, tax_code_ref):
        self.request['DefaultTaxCodeRef'] = tax_code_ref.request
        return self

    def display_name(self, value):
        self.sanitize_length('DisplayName', value, 100)
        self.request['DisplayName'] = value
        return self

    def family_name(self, value):
        self.request['FamilyName'] = value
        return self

    def fax(self, telephone_number_builder):
        self.request['Fax'] = telephone_number_builder.request
        return self

    def fully_qualified_name(self, value):
        self.request['FullyQualifiedName'] = value
        return self

    def given_name(self, value):
        self.request['GivenName'] = value
        return self

    def middle_name(self, value):
        self.request['MiddleName'] = value
        return self

    def mobile(self, telephone_number_builder):
        self.request['Mobile'] = telephone_number_builder.request
        return self

    def notes(self, value):
        self.request['Notes'] = value
        return self

    def primary_email_address(self, email_address_builder):
        self.request['PrimaryEmailAddr'] = email_address_builder.request
        return self

    def primary_phone(self, telephone_number_builder):
        self.request['PrimaryPhone'] = telephone_number_builder.request
        return self

    def print_on_check_name(self, value):
        self.sanitize_length('PrintOnCheckName', value, 100)
        self.request['PrintOnCheckName'] = value
        return self

    def shipping_address(self, physical_address_builder):
        self.request['ShipAddr'] = physical_address_builder.request
        return self

    def suffix(self, value):
        self.request['Suffix'] = value
        return self

    def taxable(self, value):
        self.request['Taxable'] = value
        return self

    def title(self, value):
        self.request['Title'] = value
        return self

    def web_address(self, web_address_builder):
        self.request['WebAddr'] = web_address_builder.request
        return self

    def currency_ref(self, currency_ref_builder):
        self.request['CurrencyRef'] = currency_ref_builder.request
        return self


class InvoiceRequestBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)
        self.request['Line'] = []

    def add_line(self, line_request_builder):
        self.request['Line'].append(line_request_builder.request)
        return self

    def customer_ref(self, customer_ref_builder):
        self.request['CustomerRef'] = customer_ref_builder.request
        return self

    def transaction_tax_detail(self, transaction_tax_detail_builder):
        self.request['TxnTaxDetail'] = transaction_tax_detail_builder.request
        return self


class ItemRequestBuilder(BaseBuilder):
    TYPE_SET = set(['Inventory', 'Service'])

    def __init__(self):
        BaseBuilder.__init__(self)

    def active(self, value):
        self.request['Active'] = value
        return self

    def taxable(self, value):
        self.request['Taxable'] = value
        return self

    def name(self, value):
        self.sanitize_length('Name', value, 100)
        self.request['Name'] = value
        return self

    def description(self, value):
        self.sanitize_length('Description', value, 4000)
        self.request['Description'] = value
        return self

    def unit_price(self, value):
        self.request['UnitPrice'] = value
        return self

    def type(self, value):
        self.sanitize_from_set('Type', value, ItemRequestBuilder.TYPE_SET)
        self.request['Type'] = value
        return self

    def income_account_ref(self, account_ref):
        self.request['IncomeAccountRef'] = account_ref.request
        return self

    def expense_account_ref(self, account_ref):
        self.request['ExpenseAccountRef'] = account_ref.request
        return self

    def asset_account_ref(self, account_ref):
        self.request['AssetAccountRef'] = account_ref.request
        return self

    def purchase_description(self, value):
        self.sanitize_length('Description', value, 1000)
        self.request['PurchaseDesc'] = value
        return self

    def purchase_cost(self, value):
        self.request['PurchaseCost'] = value
        return self



class TaxServiceRequestBuilder(BaseBuilder):

    def __init__(self):
        BaseBuilder.__init__(self)
        self.request['TaxRateDetails'] = []

    def tax_code(self, value):
        self.request['TaxCode'] = value
        return self

    def add_rate_detail(self, tax_rate_details_builder):
        self.request['TaxRateDetails'].append(tax_rate_details_builder.request)
        return self


class PaymentRequestBuilder(BaseBuilder):

    def __init__(self):
        BaseBuilder.__init__(self)
        self.request['Line'] = []

    def customer_ref(self, customer_ref_builder):
        self.request['CustomerRef'] = customer_ref_builder.request
        return self

    def ar_account_ref(self, account_ref_builder):
        self.request['ARAccountRef'] = account_ref_builder.request
        return self

    def deposit_to_account_ref(self, account_ref_builder):
        self.request['DepositToAccountRef'] = account_ref_builder.request
        return self

    def total_amount(self, value):
        self.request['TotalAmt'] = value
        return self

    def transaction_date(self, date):
        self.request['TxnDate'] = BaseBuilder.convert_date(date)
        return self

    def line(self, line_builder):
        self.request['Line'].append(line_builder.request)
        return self


class SalesReceiptRequestBuilder(BaseBuilder):
    PAYMENT_TYPE_SET = set(['Cash', 'Check', 'CreditCard', 'Other'])

    def __init__(self):
        BaseBuilder.__init__(self)
        self.request['Line'] = []

    def customer_ref(self, customer_ref_builder):
        self.request['CustomerRef'] = customer_ref_builder.request
        return self

    def private_note(self, value):
        self.sanitize_length('PrivateNote', value, 4000)
        self.request['PrivateNote'] = value
        return self

    def document_number(self, value):
        self.sanitize_length('DocNumber', value, 21)
        self.request['DocNumber'] = value
        return self

    def transaction_date(self, date):
        self.request['TxnDate'] = BaseBuilder.convert_date(date)
        return self

    def payment_type(self, value):
        self.sanitize_from_set('PaymentType', value, SalesReceiptRequestBuilder.PAYMENT_TYPE_SET)
        self.request['PaymentType'] = value
        return self

    def payment_method_ref(self, payment_method_ref_builder):
        self.request['PaymentMethodRef'] = payment_method_ref_builder.request
        return self

    def payment_ref_number(self, value):
        self.sanitize_length('PaymentRefNum', value, 21)
        self.request['PaymentRefNum'] = value
        return self

    def transaction_tax_detail(self, transaction_tax_detail_builder):
        self.request['TxnTaxDetail'] = transaction_tax_detail_builder.request
        return self

    def add_line(self, line_builder):
        self.request['Line'].append(line_builder.request)
        return self

    def deposit_to_account_ref(self, account_ref_builder):
        self.request['DepositToAccountRef'] = account_ref_builder.request
        return self

    def currency_ref(self, currency_ref_builder):
        self.request['CurrencyRef'] = currency_ref_builder.request
        return self

    def total_amount(self, value):
        self.request['TotalAmt'] = value
        return self


class TransactionTaxDetailBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def tax_code_ref(self, tax_code_ref_builder):
        self.request['TxnTaxCodeRef'] = tax_code_ref_builder.request
        return self

    def total_tax(self, value):
        self.request['TotalTax'] = value
        return self


class PhysicalAddressBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def line1(self, value):
        self.request['Line1'] = value
        return self

    def line2(self, value):
        self.request['Line2'] = value
        return self

    def line3(self, value):
        self.request['Line3'] = value
        return self

    def line4(self, value):
        self.request['Line4'] = value
        return self

    def line5(self, value):
        self.request['Line5'] = value
        return self

    def city(self, value):
        self.request['City'] = value
        return self

    def country(self, value):
        self.request['Country'] = value
        return self

    def country_sub_division_code(self, value):
        self.request['CountrySubDivisionCode'] = value
        return self

    def postal_code(self, value):
        self.request['PostalCode'] = value
        return self

    def note(self, value):
        self.request['Note'] = value
        return self

    def lat(self, value):
        self.request['Lat'] = value
        return self

    def long(self, value):
        self.request['Long'] = value
        return self


class TelephoneNumberBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def free_form_number(self, value):
        self.sanitize_length('FreeFormNumber', value, 21)
        self.request['FreeFormNumber'] = value
        return self


class EmailAddressBuilder():
    def __init__(self):
        BaseBuilder.__init__(self)

    def address(self, value):
        self.sanitize_length('Address', value, 100)
        self.request['Address'] = value
        return self


class WebSiteAddressBuilder():
    def __init__(self):
        BaseBuilder.__init__(self)

    def uri(self, value):
        self.sanitize_length('URI', value, 1000)
        self.request['URI'] = value
        return self

#region LineBuilder
class LineBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)
        self.request['LinkedTxn'] = []

    def id(self, value):
        """Required for update."""
        self.request['Id'] = value
        return self

    def amount(self, value):
        self.request['Amount'] = value
        return self

    def description(self, value):
        self.request['Description'] = value
        return self

    def add_linked_transaction(self, linked_transaction_builder):
        self.request['LinkedTxn'].append(linked_transaction_builder.request)
        return self

class InvoiceLineBuilder(LineBuilder):
    def __init__(self):
        LineBuilder.__init__(self)

    def __detail_type(self, value):
        self.request['DetailType'] = value
        return self


class SalesItemLineBuilder(InvoiceLineBuilder):

    def __init__(self):
        LineBuilder.__init__(self)
        self.request['DetailType'] = 'SalesItemLineDetail'

    def sales_item_line_detail(self, sales_item_line_detail_builder):
        self.request['SalesItemLineDetail'] = sales_item_line_detail_builder.request
        return self


class SalesItemLineDetailBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def item_ref(self, ref_builder):
        self.request['ItemRef'] = ref_builder.request
        return self

    def tax_code_ref(self, ref_builder):
        self.request['TaxCodeRef'] = ref_builder.request
        return self

    def unit_price(self, value):
        self.request['UnitPrice'] = value
        return self

    def quantity(self, value):
        self.request['Qty'] = value
        return self


#endregion

class LinkedTransactionBuilder(BaseBuilder):
    TYPE_SET = set(['APCreditCard','ARRefundCreditCard','Bill','BillPaymentCheck','BuildAssembly','CarryOver',
                    'CashPurchase','Charge','Check','CreditMemo','Deposit','EFPLiabilityCheck','EFTBillPayment',
                    'EFTRefund','Estimate','InventoryAdjustment','InventoryTransfer','Invoice','ItemReceipt',
                    'JournalEntry','LiabilityAdjustment','Paycheck','PayrollLiabilityCheck','Purchase','PurchaseOrder',
                    'PriorPayment','ReceivePayment','RefundCheck','RefundReceipt','SalesOrder','SalesReceipt',
                    'SalesTaxPaymentCheck','Transfer','TimeActivity','VendorCredit','YTDAdjustment'])

    def __init__(self):
        BaseBuilder.__init__(self)

    def id(self, value):
        self.request['TxnId'] = value
        return self

    def type(self, value):
        self.sanitize_from_set('TxnType', value, LinkedTransactionBuilder.TYPE_SET)
        self.request['TxnType'] = value
        return self

    def line_id(self, value):
        self.request['TxnLineId'] = value
        return self


class TaxRateDetailsBuilder(BaseBuilder):

    def __init__(self):
        BaseBuilder.__init__(self)

    def name(self, value):
        self.request['TaxRateName'] = value
        return self

    def rate_id(self, value):
        self.request['TaxRateId'] = value
        return self

    def rate(self, value):
        self.request['RateValue'] = value
        return self

    def agency_id(self, value):
        self.request['TaxAgencyId'] = value
        return self

    def applicable_on_sales(self):
        self.__applicable_on('Sales')
        return self

    def applicable_on_purchase(self):
        self.__applicable_on('Purchase')
        return self

    def __applicable_on(self, value):
        self.request['TaxApplicableOn'] = value


#region ReferenceBuilder
class CurrencyRefBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def name(self, value):
        self.request['name'] = value
        return self

    def value(self, value):
        self.request['value'] = value
        return self


class RefBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def name(self, value):
        """Name (Optional)."""
        self.request['name'] = value
        return self

    def type(self, value):
        self.request['type'] = value
        return self

    def value(self, value):
        """Reference object Id."""
        self.request['value'] = value
        return self


class ItemRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)


class CustomerRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)


class AccountRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)


class TaxCodeRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)

class PaymentMethodRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)
#endregion


