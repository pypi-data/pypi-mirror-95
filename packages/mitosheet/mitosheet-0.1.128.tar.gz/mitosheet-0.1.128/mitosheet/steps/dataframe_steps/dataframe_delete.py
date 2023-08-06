#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Deletes a dataframe from everywhere in the step.
"""

DATAFRAME_DELETE_EVENT = 'dataframe_delete_edit'
DATAFRAME_DELETE_STEP_TYPE = 'dataframe_delete'

DATAFRAME_DELETE_PARAMS = [
    'sheet_index',
    'old_dataframe_name'
]

def saturate_dataframe_delete(
        wsc,
        event
    ):
    """
    Adds the old dataframe name to the dataframe_delete event
    """
    sheet_index = event['sheet_index']
    old_dataframe_name = wsc.curr_step['df_names'][sheet_index]
    event['old_dataframe_name'] = old_dataframe_name


def execute_dataframe_delete(
        wsc,
        sheet_index,
        old_dataframe_name
    ):
    """
    Deletes the dataframe as sheet index.
    """
    # Create a new step and save the parameters
    wsc._create_and_checkout_new_step(DATAFRAME_DELETE_STEP_TYPE)

    # Save the parameters
    wsc.curr_step['sheet_index'] = sheet_index
    wsc.curr_step['old_dataframe_name'] = old_dataframe_name

    # Execute the delete
    wsc.curr_step['column_metatype'].pop(sheet_index)
    wsc.curr_step['column_type'].pop(sheet_index)
    wsc.curr_step['column_spreadsheet_code'].pop(sheet_index)
    wsc.curr_step['added_columns'].pop(sheet_index)
    wsc.curr_step['column_python_code'].pop(sheet_index)
    wsc.curr_step['column_evaluation_graph'].pop(sheet_index)
    wsc.curr_step['column_filters'].pop(sheet_index)
    wsc.curr_step['dfs'].pop(sheet_index)
    wsc.curr_step['df_names'].pop(sheet_index)

def transpile_dataframe_delete(
        widget_state_container,
        step,
        sheet_index,
        old_dataframe_name
    ):
    """
    Transpiles a delete step (which doesn't do much, in fairness).
    """
    return [f'del {old_dataframe_name}']


DATAFRAME_DELETE_STEP = {
    'step_version': 1,
    'event_type': DATAFRAME_DELETE_EVENT,
    'step_type': DATAFRAME_DELETE_STEP_TYPE,
    'params': DATAFRAME_DELETE_PARAMS,
    'saturate': saturate_dataframe_delete,
    'execute': execute_dataframe_delete,
    'transpile': transpile_dataframe_delete
}