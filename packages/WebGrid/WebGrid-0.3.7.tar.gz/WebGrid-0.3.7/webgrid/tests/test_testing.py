import datetime as dt
from io import BytesIO

import pytest
import xlsxwriter
import xlwt

from webgrid import testing
from webgrid_ta.grids import RadioGrid, TemporalGrid
from webgrid_ta.model.entities import Person, db


class TestAssertListEqual:
    """Verify the `assert_list_equal` method performs as expected"""

    def test_simple_equivalents(self):
        testing.assert_list_equal([], [])
        testing.assert_list_equal([1, 2, 3], [1, 2, 3])
        testing.assert_list_equal((1, 2, 3), [1, 2, 3])
        testing.assert_list_equal('123', '123')

    def test_different_lengths(self):
        with pytest.raises(AssertionError):
            testing.assert_list_equal([], [1])

        with pytest.raises(AssertionError):
            testing.assert_list_equal([1], [])

    def test_different_elements(self):
        with pytest.raises(AssertionError):
            testing.assert_list_equal([1, 2, 3], [1, 2, 4])

    def test_order_is_significant(self):
        with pytest.raises(AssertionError):
            testing.assert_list_equal([1, 2, 3], [2, 3, 1])

    def test_generators(self):
        testing.assert_list_equal((x for x in range(3)), (x for x in range(3)))
        testing.assert_list_equal((x for x in range(3)), [0, 1, 2])
        testing.assert_list_equal([0, 1, 2], (x for x in range(3)))


class TestAssertRenderedXlsMatches:
    def setup(self):
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet('sheet1')
        self.stream = BytesIO()

        self.headers_written = False

    def set_headers(self, headers):
        for index, header in enumerate(headers):
            self.sheet.write(0, index, header)

        self.headers_written = True

    def set_values(self, values):
        row_offset = 0

        if self.headers_written:
            row_offset = 1

        for row_index, row in enumerate(values, start=row_offset):
            for col_index, value in enumerate(row):
                self.sheet.write(row_index, col_index, value)

    def assert_matches(self, xls_headers, xls_rows):
        self.workbook.save(self.stream)
        testing.assert_rendered_xls_matches(self.stream.getvalue(), xls_headers, xls_rows)

    def test_empty_xls(self):
        with pytest.raises(AssertionError):
            testing.assert_rendered_xls_matches(b'', None, None)

        with pytest.raises(AssertionError):
            testing.assert_rendered_xls_matches(None, None, None)

        with pytest.raises(AssertionError):
            testing.assert_rendered_xls_matches(None, [], [])

    def test_blank_workbook(self):
        self.assert_matches([], [])

    def test_single_header(self):
        self.set_headers(['Foo'])
        self.assert_matches(['Foo'], [])

    def test_multiple_headers(self):
        self.set_headers(['Foo', 'Bar'])
        self.assert_matches(['Foo', 'Bar'], [])

    def test_single_row(self):
        self.set_values([[1, 2, 3]])
        self.assert_matches([], [[1, 2, 3]])

    def test_multiple_rows(self):
        self.set_values([
            [1, 2, 3],
            [2, 3, 4]
        ])

        self.assert_matches([], [
            [1, 2, 3],
            [2, 3, 4]
        ])

    def test_headers_and_rows(self):
        self.set_headers(['Foo', 'Bar'])
        self.set_values([
            [1, 2],
            [2, 3],
            [3, 4]
        ])

        self.assert_matches(
            ['Foo', 'Bar'],
            [
                [1, 2],
                [2, 3],
                [3, 4]
            ]
        )

    def test_value_types(self):
        self.set_values([
            [1, 1.23, 'hello', None, True, False]
        ])

        self.assert_matches([], [
            [1, 1.23, 'hello', '', True, False]
        ])

    def test_none_is_mangled(self):
        self.set_values([
            [None, 1, 1.23, 'hello', None]
        ])

        # the left `None` becomes an empty string
        # the right `None` gets dropped
        self.assert_matches([], [
            ['', 1, 1.23, 'hello']
        ])


class TestAssertRenderedXlsxMatches:
    def setup(self):
        self.stream = BytesIO()
        self.workbook = xlsxwriter.Workbook(self.stream, options={'in_memory': True})
        self.sheet = self.workbook.add_worksheet('sheet1')

        self.headers_written = None

    def set_headers(self, headers):
        assert self.headers_written is None
        self.set_values(headers)
        self.headers_written = len(headers)

    def set_values(self, values):
        row_offset = 0

        if self.headers_written:
            row_offset = self.headers_written

        for row_index, row in enumerate(values, start=row_offset):
            for col_index, value in enumerate(row):
                self.sheet.write(row_index, col_index, value)

    def assert_matches(self, xlsx_headers, xlsx_rows):
        self.workbook.close()
        testing.assert_rendered_xlsx_matches(self.workbook, xlsx_headers, xlsx_rows)

    def test_empty_xlsx(self):
        with pytest.raises(AssertionError):
            testing.assert_rendered_xlsx_matches(b'', None, None)

        with pytest.raises(AssertionError):
            testing.assert_rendered_xlsx_matches(None, None, None)

        with pytest.raises(AssertionError):
            testing.assert_rendered_xlsx_matches(None, [], [])

    def test_blank_workbook(self):
        self.assert_matches([], [])

    def test_single_header(self):
        self.set_headers([['Foo']])
        self.assert_matches([['Foo']], [])

    def test_multiple_headers(self):
        self.set_headers([['Foo', 'Bar']])
        self.assert_matches([['Foo', 'Bar']], [])

    def test_single_row(self):
        self.set_values([[1, 2, 3]])
        self.assert_matches([], [[1, 2, 3]])

    def test_multiple_rows(self):
        self.set_values([
            [1, 2, 3],
            [2, 3, 4]
        ])

        self.assert_matches([], [
            [1, 2, 3],
            [2, 3, 4]
        ])

    def test_headers_and_rows(self):
        self.set_headers([
            ['Foo', 'Bar'],
            ['Snoopy', 'Dog'],
        ])
        self.set_values([
            [1, 2],
            [2, 3],
            [3, 4]
        ])

        self.assert_matches(
            [
                ['Foo', 'Bar'],
                ['Snoopy', 'Dog'],
            ],
            [
                [1, 2],
                [2, 3],
                [3, 4]
            ]
        )

    def test_value_types(self):
        self.set_values([
            [1, 1.23, 'hello', None, True, False]
        ])

        self.assert_matches([], [
            [1, 1.23, 'hello', None, True, False]
        ])

    def test_none_is_mangled(self):
        self.set_values([
            [None, 1, 1.23, 'hello', None]
        ])

        # the right `None` gets dropped
        self.assert_matches([], [
            [None, 1, 1.23, 'hello']
        ])


@pytest.mark.skipif(db.engine.dialect.name != 'sqlite', reason='sqlite-only test')
class TestGridBase(testing.GridBase):
    grid_cls = TemporalGrid

    sort_tests = (
        ('createdts', 'persons.createdts'),
        ('due_date', 'persons.due_date'),
        ('start_time', 'persons.start_time'),
    )

    @property
    def filters(self):
        return (
            ('createdts', 'eq', dt.datetime(2018, 1, 1, 5, 30),
             "WHERE persons.createdts = '2018-01-01 05:30:00.000000'"),
            ('due_date', 'eq', dt.date(2018, 1, 1), "WHERE persons.due_date = '2018-01-01'"),
            ('start_time', 'eq', dt.time(1, 30).strftime('%I:%M %p'),
             "WHERE persons.start_time = CAST('01:30:00.000000' AS TIME)"),
        )

    def setup_method(self, _):
        Person.delete_cascaded()
        Person.testing_create(
            createdts=dt.datetime(2018, 1, 1, 5, 30),
            due_date=dt.date(2019, 5, 31),
            start_time=dt.time(1, 30),
        )

    def test_expected_rows(self):
        self.expect_table_header((('Created', 'Due Date', 'Start Time'), ))
        self.expect_table_contents((('01/01/2018 05:30 AM', '05/31/2019', '01:30 AM'), ))


@pytest.mark.skipif(db.engine.dialect.name != 'postgresql', reason='postgres-only test')
class TestGridBasePG(testing.GridBase):
    grid_cls = TemporalGrid

    sort_tests = (
        ('createdts', 'persons.createdts'),
        ('due_date', 'persons.due_date'),
        ('start_time', 'persons.start_time'),
    )

    @property
    def filters(self):
        return (
            ('createdts', 'eq', dt.datetime(2018, 1, 1, 5, 30),
             "WHERE persons.createdts = '2018-01-01 05:30:00.000000'"),
            ('due_date', 'eq', dt.date(2018, 1, 1), "WHERE persons.due_date = '2018-01-01'"),
            ('start_time', 'eq', dt.time(1, 30).strftime('%I:%M %p'),
             "WHERE persons.start_time = CAST('01:30:00.000000' AS TIME WITHOUT TIME ZONE)"),
        )


@pytest.mark.skipif(db.engine.dialect.name != 'mssql', reason='sql server-only test')
class TestGridBaseMSSQLDates(testing.MSSQLGridBase):
    grid_cls = TemporalGrid

    sort_tests = (
        ('createdts', 'persons.createdts'),
        ('due_date', 'persons.due_date'),
        ('start_time', 'persons.start_time'),
    )

    @property
    def filters(self):
        return (
            ('createdts', 'eq', dt.datetime(2018, 1, 1, 5, 30),
             "WHERE persons.createdts = '2018-01-01 05:30:00.000000'"),
            ('due_date', 'eq', '2018-01-01', "WHERE persons.due_date = '2018-01-01'"),
            ('start_time', 'eq', dt.time(1, 30).strftime('%I:%M %p'),
             "WHERE persons.start_time = CAST('01:30:00.000000' AS TIME)"),
        )


@pytest.mark.skipif(db.engine.dialect.name != 'mssql', reason='sql server-only test')
class TestGridBaseMSSQLStrings(testing.MSSQLGridBase):
    grid_cls = RadioGrid

    @property
    def filters(self):
        return (
            ('make', 'eq', 'foo', "WHERE sabwp_radios.make = 'foo'"),
            ('model', 'eq', 'foo', "WHERE sabwp_radios.model = 'foo'"),
            ('year', 'eq', '1945', "WHERE sabwp_radios.year = 1945"),
        )
