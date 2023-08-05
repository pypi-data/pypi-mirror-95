# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# Copyright (c) 2007 by PloneGov
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.MeetingCommunes.tests.testMeetingItem import testMeetingItem as mctmi
from Products.MeetingNamur.tests.MeetingNamurTestCase import MeetingNamurTestCase
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger
from Products.PloneMeeting.utils import get_annexes
from Products.PloneMeeting.utils import ON_TRANSITION_TRANSFORM_TAL_EXPR_ERROR
from Products.PloneMeeting.utils import setFieldFromAjax
from Products.statusmessages.interfaces import IStatusMessage


class testMeetingItem(MeetingNamurTestCase, mctmi):
    """
        Tests the MeetingItem class methods.
    """

    def test_pm_SendItemToOtherMCKeptFields(self):
        '''Test what fields are taken when sending to another MC, actually only fields
           enabled in both original and destination config.'''
        cfg = self.meetingConfig
        cfg2 = self.meetingConfig2
        cfg2Id = cfg2.getId()
        # enable motivation and budgetInfos in cfg1, not in cfg2
        cfg.setUsedItemAttributes(('motivation', 'budgetInfos'))
        cfg2.setUsedItemAttributes(('itemIsSigned', 'privacy'))
        cfg.setItemManualSentToOtherMCStates((self.WF_STATE_NAME_MAPPINGS['itemcreated'],))

        # create and send
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        # default always kept fields
        item.setTitle('My title')
        item.setDescription('<p>My description</p>', mimetype='text/html')
        item.setDecision('<p>My decision</p>', mimetype='text/html')
        # optional fields
        item.setMotivation('<p>My motivation</p>', mimetype='text/html')
        item.setBudgetRelated(True)
        item.setBudgetInfos('<p>My budget infos</p>', mimetype='text/html')
        item.setOtherMeetingConfigsClonableTo((cfg2Id,))
        item.at_post_edit_script()
        clonedItem = item.cloneToOtherMeetingConfig(cfg2Id)
        # make sure relevant fields are there or no more there
        # xxx Namur, Description is removed
        self.assertEquals(clonedItem.Title(), item.Title())
        self.assertEquals(clonedItem.Description(), '')
        # xxx Namur, the decision field is fill when item go to te meetingManager (validated)
        # an item who is send to other config didn't have decision
        self.assertEquals(clonedItem.getDecision(), '<p>&nbsp;</p>')
        self.failIf(clonedItem.getMotivation())
        self.failIf(clonedItem.getBudgetRelated())
        self.failIf(clonedItem.getBudgetInfos())
        self.failIf(clonedItem.getOtherMeetingConfigsClonableTo())

    def test_pm_OnTransitionFieldTransforms(self):
        ''' We must ovveride this test because for Namur, the decision field is never fill by creator or reviewer
           On transition triggered, some transforms can be applied to item or meeting
           rich text field depending on what is defined in MeetingConfig.onTransitionFieldTransforms.
           This is used for example to adapt the text of the decision when an item is delayed or refused.
           '''
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        self.decideMeeting(meeting)
        # we will adapt item decision when the item is delayed
        item1 = meeting.getItems()[0]
        originalDecision = '<p>Current item decision.</p>'
        item1.setDecision(originalDecision)
        # for now, as nothing is defined, nothing happens when item is delayed
        self.do(item1, 'delay')
        self.assertTrue(item1.getDecision(keepWithNext=False) == originalDecision)
        # configure onTransitionFieldTransforms and delay another item
        delayedItemDecision = '<p>This item has been delayed.</p>'
        self.meetingConfig.setOnTransitionFieldTransforms(
            ({'transition': 'delay',
              'field_name': 'MeetingItem.decision',
              'tal_expression': 'string:%s' % delayedItemDecision},))
        item2 = meeting.getItems()[1]
        item2.setDecision(originalDecision)
        self.do(item2, 'delay')
        self.assertTrue(item2.getDecision(keepWithNext=False) == delayedItemDecision)
        # if the item was duplicated (often the case when delaying an item), the duplicated
        # item keep the original decision
        duplicatedItem = item2.getBRefs('ItemPredecessor')[0]
        # right duplicated item
        self.assertTrue(duplicatedItem.getPredecessor() == item2)
        self.assertTrue(duplicatedItem.getDecision(keepWithNext=False) == '<p>&nbsp;</p>')
        # this work also when triggering any other item or meeting transition with every rich fields
        item3 = meeting.getItems()[2]
        self.meetingConfig.setOnTransitionFieldTransforms(
            ({'transition': 'accept',
              'field_name': 'MeetingItem.description',
              'tal_expression': 'string:<p>My new description.</p>'},))
        item3.setDescription('<p>My original description.</p>')
        self.do(item3, 'accept')
        self.assertTrue(item3.Description() == '<p>My new description.</p>')
        # if ever an error occurs with the TAL expression, the transition
        # is made but the rich text is not changed and a portal_message is displayed
        self.meetingConfig.setOnTransitionFieldTransforms(
            ({'transition': 'accept',
              'field_name': 'MeetingItem.decision',
              'tal_expression': 'some_wrong_tal_expression'},))
        item4 = meeting.getItems()[3]
        item4.setDecision('<p>My decision that will not be touched.</p>')
        self.do(item4, 'accept')
        # transition was triggered
        self.assertTrue(item4.queryState() == 'accepted')
        # original decision was not touched
        self.assertTrue(item4.getDecision(keepWithNext=False) == '<p>My decision that will not be touched.</p>')
        # a portal_message is displayed to the user that triggered the transition
        messages = IStatusMessage(self.request).show()
        self.assertTrue(messages[-1].message == ON_TRANSITION_TRANSFORM_TAL_EXPR_ERROR % (
            'decision', "'some_wrong_tal_expression'"))

    def test_pm_DuplicatedItemDoesNotKeepDecisionAnnexes(self):
        """When an item is duplicated using the 'duplicate and keep link',
           decision annexes are not kept."""
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        self.addAnnex(item)
        # xxx Namur, creator can't create "Annexe decision"
        self.changeUser('admin')
        self.addAnnex(item, relatedTo='item_decision')
        self.changeUser('pmCreator1')
        self.assertTrue(get_annexes(item, portal_types=['annex']))
        self.assertTrue(get_annexes(item, portal_types=['annexDecision']))
        # cloned and link not kept, decison annexes are removed
        clonedItem = item.clone()
        self.assertTrue(get_annexes(clonedItem, portal_types=['annex']))
        self.assertFalse(get_annexes(clonedItem, portal_types=['annexDecision']))
        # cloned but link kept, decison annexes are also removed
        clonedItemWithLink = item.clone(setCurrentAsPredecessor=True)
        self.assertTrue(get_annexes(clonedItemWithLink, portal_types=['annex']))
        self.assertFalse(get_annexes(clonedItemWithLink, portal_types=['annexDecision']))

    def test_pm_ItemExternalImagesStoredLocally(self):
        """External images are stored locally."""
        cfg = self.meetingConfig
        if 'creator_initiated_decisions' in cfg.listWorkflowAdaptations():
            cfg.setWorkflowAdaptations(('creator_initiated_decisions', ))
            performWorkflowAdaptations(cfg, logger=pm_logger)
        self.changeUser('pmCreator1')
        # creation time
        text = '<p>Working external image <img src="%s"/>.</p>' % self.external_image1
        pmFolder = self.getMeetingFolder()
        # do not use self.create to be sure that it works correctly with invokeFactory
        itemId = pmFolder.invokeFactory(cfg.getItemTypeName(),
                                        id='item',
                                        proposingGroup=self.developers_uid,
                                        description=text)
        item = getattr(pmFolder, itemId)
        item.processForm()
        # contact.png was saved in the item
        self.assertTrue('22-400x400.jpg' in item.objectIds())
        img = item.get('22-400x400.jpg')
        # external image link was updated
        self.assertEqual(
            item.getRawDescription(),
            '<p>Working external image <img src="resolveuid/{0}">.</p>'.format(img.UID()))
        # xxx Namur creator can't complete decision field continue with admin
        self.changeUser('admin')
        # test using the quickedit, test with field 'decision' where getRaw was overrided
        decision = '<p>Working external image <img src="%s"/>.</p>' % self.external_image2
        setFieldFromAjax(item, 'decision', decision)
        self.assertTrue('1025-400x300.jpg' in item.objectIds())
        img2 = item.get('1025-400x300.jpg')
        # external image link was updated
        self.assertEqual(
            item.getRawDecision(),
            '<p>Working external image <img src="resolveuid/{0}">.</p>'.format(img2.UID()))

        # test using at_post_edit_script, aka full edit form
        decision = '<p>Working external image <img src="%s"/>.</p>' % self.external_image3
        item.setDecision(decision)
        item._update_after_edit()
        self.assertTrue('1035-600x400.jpg' in item.objectIds())
        img3 = item.get('1035-600x400.jpg')
        # external image link was updated
        self.assertEqual(
            item.getRawDecision(),
            '<p>Working external image <img src="resolveuid/{0}">.</p>'.format(img3.UID()))

        # link to unknown external image, like during copy/paste of content
        # that has a link to an unexisting image or so
        decision = '<p>Not working external image <img src="https://i.picsum.photos/id/449/400.png">.</p>'
        item.setDecision(decision)
        item._update_after_edit()
        self.assertTrue('1035-600x400.jpg' in item.objectIds())
        # nothing was done
        self.assertListEqual(
            sorted(item.objectIds()),
            ['1025-400x300.jpg', '1035-600x400.jpg', '22-400x400.jpg'])
        self.assertEqual(item.getRawDecision(), decision)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from mctmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_pm_'))
    return suite
