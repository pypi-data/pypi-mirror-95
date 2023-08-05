# -*- coding: utf-8 -*-

from __future__ import print_function

from .basex import BookBase, SheetBase
from .misc import Env
from .utils import tag_test, xv_test
from .xlnode import Row, Cell, EmptyCell, TagCell, XvCell, RichTagCell, create_cell
from .xlrange import SheetRange
from .xlext import NodeExtension, SegmentExtension, XvExtension, ImageExtension, RangeExtension
from .ynext import YnExtension
from .richtexthandler import rich_handlerx


class SheetWriter(SheetBase):
    pass

class BookWriter(BookBase):

    def __init__(self, fname, debug=False, nocache=False):
        self.debug = debug
        self.load(fname)
        self.nocache = nocache

    def load(self, fname):
        BookBase.load(self, fname)
        self.prepare_env()
        self.sheet_range_list = []
        for rdsheet in self.rdsheet_list:
            sheet_range = self.get_sheet_range(rdsheet)
            if self.debug:
                print('sheet name: ', rdsheet.title)
                print('ranges specified')
                sheet_range.print()
            sheet_range.split()
            if self.debug:
                print('ranges split')
                sheet_range.print_split()
            sheet_range.rich_handler = rich_handlerx
            tpl_source = sheet_range.to_tpl()
            if self.debug:
                print('template source')
                print(tpl_source)
            jinja_tpl = self.jinja_env.from_string(tpl_source)
            self.sheet_range_list.append((sheet_range, jinja_tpl, rdsheet))

    def prepare_env(self):
        self.jinja_env = Env(extensions=[NodeExtension, SegmentExtension, YnExtension,
                                         XvExtension, ImageExtension, RangeExtension])
        self.jinja_env.xlsx = True

    def get_sheet_range(self, sheet):
        sheet_range = SheetRange(min_col=1, min_row=1, max_col=sheet.max_column,
                                 max_row=sheet.max_row, index_base=1)

        for rowx in range(1, sheet.max_row + 1):
            for colx in range(1, sheet.max_column + 1):
                source_cell = sheet._cells.get((rowx, colx))
                if not source_cell:
                    sheet_cell = EmptyCell(rowx, colx)
                    sheet_range.add_cell(sheet_cell)
                    continue

                if source_cell.comment:
                    comment = source_cell.comment.text
                    if tag_test(comment):
                        sheet_range.parse_tag(comment, rowx, colx)

                value = source_cell._value
                data_type = source_cell.data_type
                rich_text = None
                if hasattr(value, 'rich') and value.rich:
                    rich_text = value.rich
                if data_type == 's':
                    if not tag_test(value):
                        sheet_cell = Cell(rowx, colx, value, data_type)
                    else:
                        font = self.get_font(source_cell._style.fontId)
                        sheet_cell = create_cell(rowx, colx, value, rich_text, data_type, font, rich_handlerx)
                else:
                    sheet_cell = Cell(rowx, colx, value, data_type)
                sheet_range.add_cell(sheet_cell)

        return sheet_range

    def render_sheet(self, payload, sheet_name, idx):
        sheet_range, jinja_tpl, rdsheet = self.sheet_range_list[idx]
        sheet_writer = SheetWriter(self, rdsheet, sheet_name)
        self.jinja_env.sheet_pos = sheet_range.get_pos(sheet_writer, nocache=self.nocache)
        if self.debug:
            print("range positions")
            self.jinja_env.sheet_pos.print()
        rv = jinja_tpl.render(payload)
        sheet_writer.merge_finish()

    def render_book(self, payloads):
        if isinstance(payloads, dict):
            for key, payload in payloads.items():
                idx = self.get_tpl_idx(payload)
                sheet_name = self.get_sheet_name(payload, key)
                self.render_sheet(payload, sheet_name, idx)
        elif isinstance(payloads, list):
            for payload in payloads:
                idx = self.get_tpl_idx(payload)
                sheet_name = self.get_sheet_name(payload)
                self.render_sheet(payload, sheet_name, idx)

    def render_book2(self, payloads):
        for payload in payloads:
            idx = self.get_tpl_idx(payload)
            sheet_name = self.get_sheet_name(payload)
            self.render_sheet(payload['ctx'], sheet_name, idx)

    def render(self, payload):
        idx = self.get_tpl_idx(payload)
        sheet_name = self.get_sheet_name(payload)
        self.render_sheet(payload, sheet_name, idx)

    def save(self, fname):
        self.workbook.save(fname)
        for sheet in self.workbook.worksheets:
            self.workbook.remove(sheet)