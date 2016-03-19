# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

raw_comment = """I downvoted you, but I thought I&#x27;d explain why - I don&#x27;t think it&#x27;s reasonable to characterise this as childish.  Government surveillance is something which our industry is the best positioned to speak out against.  This type of thing seems to be clearly political speech, and not a prank.

    You may enjoy The Master Algorithm: <a href="http://www.amazon.com/Master-
    Algorithm-Ultimate-Learning-Machine/dp/0465065708"
    rel="nofollow">http://www.amazon.com/Master-Algorithm-Ultimate-Learning-
    Mac...</a>

    There was a great article called <i>The Space Doctor's Big Idea</i> There was a great article called <i>The Space Doctor's Big Idea</i>.

    What would a satisfactory "why" even look like exactly? As
    in, what form might it take compared to some other scientific discipline
    where we <i>do</i> know what's going on?<p>Personally, I think the whole
    thing is a red herring -- people in the field have <i>some idea</i> of how
    neural nets work, and there are many disciplines considered by many to be
    mature sciences that are far from settled on a grand theoretical
    scale.<p>That said...
"""  # NOQA

formatted_heading = '\x1b[33m\n      foo - just now\x1b[0m'

formatted_comment = """      I downvoted you, but I thought I\'d explain why - I don\'t think it\'s\n      reasonable to characterise this as childish.  Government surveillance is\n      something which our industry is the best positioned to speak out\n      against.  This type of thing seems to be clearly political speech, and\n      not a prank.\n\n    You may enjoy The Master Algorithm: <a\n      href="http://www.amazon.com/Master-\n    Algorithm-Ultimate-Learning-\n      Machine/dp/0465065708"\n    rel="nofollow">http://www.amazon.com/Master-\n      Algorithm-Ultimate-Learning-\n    Mac...</a>\n\n    There was a great\n      article called \x1b[36m<i>The Space Doctor\'s Big Idea</i>\x1b[0m There was a\n      great article called \x1b[36m<i>The Space Doctor\'s Big Idea</i>\x1b[0m.\n      What would a satisfactory "why" even look like exactly? As\n    in, what\n      form might it take compared to some other scientific discipline\n      where we \x1b[36m<i>do</i>\x1b[0m know what\'s going on?\n\n      \x1b[0mPersonally,\n      I think the whole\n    thing is a red herring -- people in the field have\n      \x1b[36m<i>some idea</i>\x1b[0m of how\n    neural nets work, and there are\n      many disciplines considered by many to be\n    mature sciences that are\n      far from settled on a grand theoretical\n    scale.\n\n      \x1b[0mThat\n      said..."""  # NOQA
