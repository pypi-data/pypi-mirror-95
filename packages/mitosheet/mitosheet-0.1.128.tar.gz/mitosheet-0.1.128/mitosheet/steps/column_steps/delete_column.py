#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A delete_column step, which allows you to delete a column
from a dataframe.
"""

from mitosheet.errors import (
    make_no_sheet_error,
    make_no_column_error,
    make_invalid_column_delete_error
)

DELETE_COLUMN_EVENT = 'delete_column_edit'
DELETE_COLUMN_STEP_TYPE = 'delete_column'

DELETE_COLUMN_PARAMS = [
    'sheet_index', # the sheet to delete the column from
    'column_header', # the column to delete
]

def execute_delete_column_step(
        wsc,
        sheet_index,
        column_header
    ):
    """
    Creates a new step that deletes a the column column_heder 
    from the sheet at sheet_index.
    """

    # if the sheet doesn't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    # Error if the column does not exist
    if column_header not in wsc.curr_step['column_metatype'][sheet_index]:
        raise make_no_column_error([column_header])
    
    # Error if there are any columns that currently rely on this column
    if len(wsc.curr_step['column_evaluation_graph'][sheet_index][column_header]) > 0:
        raise make_invalid_column_delete_error(
            column_header,
            list(wsc.curr_step['column_evaluation_graph'][sheet_index][column_header])
        )

    # Make a new step for the delete
    wsc._create_and_checkout_new_step(DELETE_COLUMN_STEP_TYPE)
    
    # Actually drop the column
    df = wsc.curr_step['dfs'][sheet_index]
    df.drop(column_header, axis=1, inplace=True)

    # And then update all the state variables removing this column from the state
    del wsc.curr_step['column_metatype'][sheet_index][column_header]
    del wsc.curr_step['column_type'][sheet_index][column_header]
    del wsc.curr_step['column_spreadsheet_code'][sheet_index][column_header]
    del wsc.curr_step['column_python_code'][sheet_index][column_header]
    del wsc.curr_step['column_evaluation_graph'][sheet_index][column_header]
    # We also have to delete the places in the graph where this node is 
    for dependents in wsc.curr_step['column_evaluation_graph'][sheet_index].values():
        if column_header in dependents:
            dependents.remove(column_header)


def transpile_delete_column_step(
        widget_state_container,
        step,
        sheet_index,
        column_header
    ):
    df_name = step['df_names'][sheet_index]
    return [f'{df_name}.drop(\'{column_header}\', axis=1, inplace=True)']


DELETE_COLUMN_STEP = {
    'step_version': 1,
    'event_type': DELETE_COLUMN_EVENT,
    'step_type': DELETE_COLUMN_STEP_TYPE,
    'params': DELETE_COLUMN_PARAMS,
    'saturate': None,
    'execute': execute_delete_column_step,
    'transpile': transpile_delete_column_step
}