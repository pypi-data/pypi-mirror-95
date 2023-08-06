# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009 Jeff Hammel <jhammel@openplans.org>
# Copyright (C) 2012 Ryan J Ollos <ryan.j.ollos@gmail.com>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from trac.config import ListOption
from trac.core import Component, implements
from trac.ticket.model import _fixup_cc_list
from trac.ticket.web_ui import TicketModule
from trac.util import as_bool
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
        if as_bool(req.args.get('users', '1')):
            subjects.extend(self._get_users(req))

        if as_bool(req.args.get('groups')):
            subjects.extend(self._get_groups(req))

        content = to_json(subjects)
        req.send(content, 'application/json', 200)

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [('autocompleteusers', resource_filename(__name__, 'htdocs'))]

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
            fields = []
            multi_fields = []
            add_script(req, 'autocompleteusers/js/autocomplete.js')
            subjects_href = req.href.subjects()
            if template == 'ticket.html':
                fields = [
                    '#field-owner',
                    'input:text#field-reporter',
                    '#action input:text[id$=_reassign_owner]',
                    '.trac-autocomplete'
                ]
                multi_fields = [
                    '#field-cc',
                ]
            elif template == 'admin_perms.html':
                subjects_href += '?groups=1'
                fields = [
                    '#cp_subject',
                    '#cp_target',
                    '#gp_subject',
                    '#sg_subject',
                    '#sg_group',
                ]
            elif template == 'query.html':
                fields = []
                multi_fields = []
                add_script(req, 'autocompleteusers/js/autocomplete_query.js')

            add_script_data(req, {
                'autocomplete_fields':
                    self.config.getlist(SECTION_NAME, FIELDS_OPTION[0]) +
                    fields,
                'autocomplete_fields_multi':
                    self.config.getlist(SECTION_NAME, FIELDS_OPTION[1]) +
                    multi_fields,
                'subjects_href': subjects_href,
            })
        return template, data, content_type

    # Private methods

    def _get_groups(self, req):
        # Returns a list of groups by filtering users with session data
        # from the list of all subjects. This has the caveat of also
        # returning users without session data, but there currently seems
        # to be no other way to handle this.
        query = req.args.get('q', '').lower()
        db = self.env.get_read_db()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT username FROM permission")
        perm_users = [row[0] for row in cursor]
        known_users = set(item[0] for item in self.env.get_known_users())
        return sorted([user, None, None] for user in perm_users
                      if user not in known_users and
                      user.lower().startswith(query))

    def _get_users(self, req):
        # instead of known_users, could be
        # perm = PermissionSystem(self.env)
        # owners = perm.get_users_with_permission('TICKET_MODIFY')
        # owners.sort()
        # see: https://trac.edgewall.org/browser/trunk/trac/ticket/default_workflow.py#L232

        query = req.args.get('q', '').lower()

        # user names, email addresses, full names
        can_view = Chrome(self.env).show_email_addresses or \
            'EMAIL_VIEW' in req.perm
        users = []
        for user_data in self.env.get_known_users():
            user_data = [value or '' for value in user_data]
            if not can_view and user_data[EMAIL]:
                user_data[EMAIL] = obfuscate_email_address(user_data[EMAIL])
            for field in xrange(0, 3):  # ordered by how they appear
                value = user_data[field].lower()

                if value.startswith(query):
                    users.append(user_data)
                    break
                if field == NAME:
                    lastnames = value.split()[1:]
                    if sum(name.startswith(query) for name in lastnames):
                        users.append(user_data)
                        break

        return sorted(users)
