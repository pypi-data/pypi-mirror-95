# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009 Jeff Hammel <jhammel@openplans.org>
# Copyright (C) 2012 Ryan J Ollos <ryan.j.ollos@gmail.com>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from trac.config import ListOption
from trac.core import Component, implements
from trac.env import Environment
from trac.ticket.model import _fixup_cc_list
from trac.ticket.web_ui import TicketModule
from trac.util.presentation import to_json
from trac.util.text import obfuscate_email_address
from trac.web.api import IRequestFilter, IRequestHandler
from trac.web.chrome import Chrome, ITemplateProvider
from trac.web.chrome import add_script, add_script_data, add_stylesheet


USER = 0
NAME = 1
EMAIL = 2  # indices

SECTION_NAME = 'autocomplete'
FIELDS_OPTION = ('fields', 'multi_fields')
SCRIPT_FIELD_NAME = 'autocomplete_fields'


class AutocompleteUsers(Component):
    implements(IRequestFilter, IRequestHandler, ITemplateProvider)

    complete_fields = ListOption(
        SECTION_NAME, FIELDS_OPTION[0], default='',
        doc="Select fields to autocomplete")

    multi_complete_fields = ListOption(
        SECTION_NAME, FIELDS_OPTION[1], default='',
        doc="""Select fields to autocomplete with multiple
        (comma-separated) values.
        """)

    # IRequestHandler methods

    def match_request(self, req):
        return req.path_info.rstrip('/') == '/subjects'

    def process_request(self, req):

        subjects = []
        if req.args.get('users', '1') == '1':
            users = self._get_users(req)
            subjects = [(user[USER],
                         user[EMAIL] and '<%s> ' % user[EMAIL] or '',
                         user[NAME])
                        for value, user in users]  # value unused (placeholder needed for sorting)

        if req.args.get('groups'):
            groups = self._get_groups(req)
            if groups:
                subjects.extend((group, '', 'group') for group in groups)

        content = to_json(subjects)
        if isinstance(content, unicode):
            content = content.encode('utf-8')
        req.send(content, 'application/json')

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename

        return [('autocomplete', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return []

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        if handler is self.env.components[TicketModule] and \
                req.method == 'POST':

            def fixup_user_list(option_name):
                for field in self.config.getlist(SECTION_NAME, option_name):
                    arg = 'field_' + field
                    if arg in req.args:
                        req.args[arg] = _fixup_cc_list(req.args[arg])

            fixup_user_list(FIELDS_OPTION[0])
            fixup_user_list(FIELDS_OPTION[1])
        return handler

    def post_process_request(self, req, template, data, content_type):
        if template in ('ticket.html', 'admin_perms.html', 'query.html'):
            Chrome(self.env).add_jquery_ui(req)
            add_stylesheet(req, 'autocomplete/css/autocompleteusers.css')
            add_script(req, 'autocomplete/js/autocompleteusers.js')
            script_data = {
                'template': template,
                'fields': self.complete_fields,
                'multi_fields': self.multi_complete_fields,
                'url': req.href.subjects(),
            }
            add_script_data(req, {'autocompleteusers': script_data})
        return template, data, content_type

    # Private methods

    def _get_groups(self, req):
        # Returns a list of groups by filtering users with session data
        # from the list of all subjects. This has the caveat of also
        # returning users without session data, but there currently seems
        # to be no other way to handle this.
        query = req.args.get('term', '').lower()
        perm_users = self._get_perm_users()
        known_users = set(item[0] for item in self.env.get_known_users())
        return sorted(user for user in perm_users
                      if user not in known_users and
                      user.lower().startswith(query))

    if hasattr(Environment, 'db_query'):
        def _get_perm_users(self):
            with self.env.db_query as db:
                cursor = db.cursor()
                cursor.execute("SELECT DISTINCT username FROM permission")
                return [row[0] for row in cursor]
    else:
        def _get_perm_users(self):
            db = self.env.get_read_db()
            cursor = db.cursor()
            cursor.execute("SELECT DISTINCT username FROM permission")
            return [row[0] for row in cursor]

    def _get_users(self, req):
        # instead of known_users, could be
        # perm = PermissionSystem(self.env)
        # owners = perm.get_users_with_permission('TICKET_MODIFY')
        # owners.sort()
        # see: http://trac.edgewall.org/browser/trunk/trac/ticket/default_workflow.py#L232

        query = req.args.get('term', '').lower()

        # user names, email addresses, full names
        can_view = Chrome(self.env).show_email_addresses or \
            'EMAIL_VIEW' in req.perm
        users = []
        for user_data in self.env.get_known_users():
            user_data = [value or '' for value in user_data]
            if not can_view and user_data[EMAIL]:
                user_data[EMAIL] = obfuscate_email_address(user_data[EMAIL])
            for index, field in enumerate((USER, EMAIL, NAME)):  # ordered by how they appear
                value = user_data[field].lower()

                if value.startswith(query):
                    users.append((2 - index, user_data))  # 2-index is the sort key
                    break
                if field == NAME:
                    lastnames = value.split()[1:]
                    if sum(name.startswith(query) for name in lastnames):
                        users.append((2 - index, user_data))  # 2-index is the sort key
                        break

        return sorted(users)
