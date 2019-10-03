# -*- coding: utf-8 -*-
# @Author: Catofes
# @Date:   2015-08-15
'''
Class to stores everything into a json file.
'''
from nemcore.pdict import PersistentDict


class Storage(PersistentDict):
    def login(self, account=None, profile=None):
        assert account, 'keyword argument account should never been None'
        assert profile, 'keyword argument profile should never been None'
        self.data['user'] = {'account': account, 'profile': profile}
        self.save()

    def logout(self):
        self.data['user'] = {}
        self.save()

    @property
    def uid(self):
        return self.data.get('user', {}).get('profile', {}).get('userId', None)
