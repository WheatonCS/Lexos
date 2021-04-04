# This file is used by the TestHandleGutenberg class in
#   test.unit_test.test_scrubber.py

FRONT_PLATE = "'The Project Gutenberg EBook of Pride and Prejudice, by Jane" \
              " Austen\n\nThis eBook is for the use of anyone anywhere at no" \
              " cost and with\nalmost no restrictions whatsoever.  You may " \
              "copy it, give it away or\nre-use it under the terms of the " \
              "Project Gutenberg License included\nwith this eBook or online" \
              " at www.gutenberg.org\n\nTitle: Pride and Prejudice\n\n" \
              "Author: Jane Austen\n\nPosting Date: August 26, 2008 [EBook" \
              " #1342]\nRelease Date: June, 1998\nLast Updated: October 17," \
              " 2016\n\nLanguage: English\n\nCharacter set encoding: " \
              "UTF-8\n\n*** START OF THIS PROJECT GUTENBERG EBOOK PRIDE " \
              "AND PREJUDICE ***"

FRONT_PLATE_ALT = "\nThe Project Gutenberg EBook of The Strange Case Of " \
                  "Dr. Jekyll And Mr.\nHyde, by Robert Louis Stevenson\n\n"\
                  "This eBook is for the use of anyone anywhere at no cost" \
                  " and with\nalmost no restrictions whatsoever.You may " \
                  "copy it, give it away or\nre-use it under the terms " \
                  "of the Project Gutenberg License included\nwith this " \
                  "eBook or online at www.gutenberg.org\n\n\nTitle: " \
                  "The Strange Case Of Dr. Jekyll And Mr. Hyde\n\n" \
                  "Author: Robert Louis Stevenson\n\nRelease Date: " \
                  "June 25, 2008 [EBook #43]\nLast Updated: December 6, " \
                  "2018\n\nLanguage: English\n\nCharacter set encoding: " \
                  "UTF-8\n\n*** START OF THIS PROJECT GUTENBERG EBOOK\n" \
                  "THE STRANGE CASE OF DR. JEKYLL AND MR. HYDE ***" \

FRONT_PLATE_OUTDATED = "***The Project Gutenberg's Etext of Shakespeare's" \
                       " First Folio***\n********************The Tragedie" \
                       " of Macbeth*********************\n\n***The Projec" \
                       "t Gutenberg's Etext of Shakespeare's First Folio*" \
                       "**********************The Tragedie of Macbeth****" \
                       "*****************\n\n\n***START**THE SMALL PRINT" \
                       "!**FOR PUBLIC DOMAIN ETEXTS**START***\nWhy is thi" \
                       "s 'Small Print!' statement here?  You know: lawye" \
                       "rs.\n\netext possible.\n\n***\n\n\nScanner's Notes:" \
                       " What this is and isn't.  This was taken from\n" \
                       "a copy of Shakespeare's first folio and it is as " \
                       "close as I can\ncome in ASCII to the printed text.\n" \
                       "  My email address for right " \
                       "now are haradda@aol.comand davidr@inconnect.com.\n  " \
                       "I hope that you enjoy this.\n\nDavid Reed\n"

# removes 'David Reed' at end of string
FRONT_PLATE_OUTDATED_WRONG = \
                    FRONT_PLATE_OUTDATED[:len(FRONT_PLATE_OUTDATED) - 11]

FRONT_PLATE_EXTRA = "\n\nProduced by Anonymous Volunteers\n\nPRIDE AND " \
                    "PREJUDICE\n\nBy Jane Austen\n\n"

TEXT_NEITHER = "Chapter 1\n\nIt is a truth universally acknowledged, that a" \
               " single man in possession\nof a good fortune, must be in" \
               " want of a wife.\n\n<much text goes here>\n\n*** Testing" \
               " stars ***\n\nWith the Gardiners, they were always on the "\
               " most intimate terms.\nDarcy, as well as Elizabeth, really "\
               "loved them; and they were both ever\nsensible of the warmest" \
               " gratitude towards the persons who, by bringing\nher into "\
               " Derbyshire, had been the means of uniting them.\n\n"


BACK_PLATE = "End of the Project Gutenberg EBook of Pride and Prejudice, by" \
             " Jane Austen\n\n*** END OF THIS PROJECT GUTENBERG EBOOK PRIDE" \
             " AND PREJUDICE ***\n\n***** This file should be named " \
             "1342-0.txt or 1342-0.zip *****\nThis and all associated files" \
             " of various formats will be found in:\n" \
             "        http://www.gutenberg.org/1/3/4/1342/\n\nProduced by" \
             " Anonymous Volunteers\n\nUpdated editions will replace the" \
             " previous one--the old editions\nwill be renamed." \
             "\n\n<explanation of public domain goes here>\n\n*** START:" \
             " FULL LICENSE ***\n\nTHE FULL PROJECT GUTENBERG LICENSE\n" \
             "PLEASE READ THIS BEFORE YOU DISTRIBUTE OR USE THIS WORK\n\n" \
             "<much license goes here>\n\nMost people start at our Web site" \
             " which has the main PG search facility:\n\n     " \
             "http://www.gutenberg.org\n\nThis Web site includes information" \
             " about Project Gutenberg-tm,\nincluding how to make donations" \
             " to the Project Gutenberg Literary\nArchive Foundation, how to" \
             " help produce our new eBooks, and how to\nsubscribe to our" \
             " email newsletter to hear about new eBooks.\n\n"

TEXT_FRONT_PLATE = FRONT_PLATE + FRONT_PLATE_EXTRA + TEXT_NEITHER
TEXT_FRONT_PLATE_ALT = FRONT_PLATE_ALT + FRONT_PLATE_EXTRA + TEXT_NEITHER
TEXT_FRONT_PLATE_OUTDATED = FRONT_PLATE_OUTDATED + FRONT_PLATE_EXTRA + \
                            TEXT_NEITHER
TEXT_FRONT_PLATE_OUTDATED_WRONG = FRONT_PLATE_OUTDATED_WRONG + \
                            FRONT_PLATE_EXTRA + TEXT_NEITHER
TEXT_BACK = TEXT_NEITHER + BACK_PLATE
TEXT_BOTH_PLATE = TEXT_FRONT_PLATE + BACK_PLATE
