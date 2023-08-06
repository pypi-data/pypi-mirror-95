#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A sort step, which allows you to sort a df based on some key column
"""
import pandas as pd

from mitosheet.errors import (
    EditError,
    make_execution_error,
    make_no_sheet_error,
    make_no_column_error,
    make_invalid_sort_error
)

SORT_EVENT = 'sort_edit'
SORT_STEP_TYPE = 'sort'

SORT_COLUMN_PARAMS = [
    'sheet_index', # int
    'column_header', # column to sort
    'sort_direction' # string either 'ascending' or 'descending'
]

# CONSTANTS USED IN THE SORT STEP ITSELF
ASCENDING = 'ascending'
DESCENDING = 'descending'

def execute_sort(
        wsc,
        sheet_index,
        column_header,
        sort_direction,
    ):
    """
    sorts an existing sheet with the given sort_direction on the column_header
    """
    # if the sheet doesn't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the sorted column exists 
    missing_column = set([column_header]).difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if len(missing_column) > 0: 
        raise make_no_column_error(missing_column)

    # If no errors we create a new step for this sort
    wsc._create_and_checkout_new_step(SORT_STEP_TYPE)

    # execute on real dataframes
    wsc.dfs[sheet_index] = _execute_sort(
        wsc.dfs[sheet_index], 
        column_header,
        sort_direction
    )

def _execute_sort(
        df,
        column_header,
        sort_direction,
    ):
    """
    Executes a sort on the given df, by sorting the column named 
    column_header in sort_direction (ascending or descending)
    """

    try: 
        new_df = df.sort_values(by=column_header, ascending=(sort_direction == ASCENDING), na_position='first')
        return new_df.reset_index(drop=True)
    except TypeError as e:
        # A NameError occurs when you try to sort a column with incomparable 
        # dtypes (ie: a column with strings and floats)
        print(e)
        # Generate an error informing the user
        raise make_invalid_sort_error(column_header)


def transpile_sort(
        widget_state_container,
        step,
        sheet_index,
        column_header,
        sort_direction
    ):
    """
    Transpiles a sort step to Python code. 
    """
    # sort the dataframe
    df_name = step["df_names"][sheet_index]
    sort_line = f'{df_name} = {df_name}.sort_values(by=\'{column_header}\', ascending={sort_direction == ASCENDING}, na_position=\'first\')'
    reset_index_line = f'{df_name} = {df_name}.reset_index(drop=True)'

    return [sort_line, reset_index_line]


SORT_STEP = {
    'step_version': 1,
    'event_type': SORT_EVENT,
    'step_type': SORT_STEP_TYPE,
    'params': SORT_COLUMN_PARAMS,
    'saturate': None,
    'execute': execute_sort,
    'transpile': transpile_sort
}