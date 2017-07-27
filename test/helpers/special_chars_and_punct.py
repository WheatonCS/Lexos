# This file is used by the TestMakeReplacer test class in
#   test.unit_test.test_scrubber.py
# This file is NOT to be used for special char conversion in the Lexos app!!!

EE_HTML = {'&ae;': 'æ', '&d;': 'ð', '&t;': 'þ', '&e;': 'ę', '&AE;': 'Æ',
           '&D;': 'Ð', '&T;': 'Þ', '&#541;': 'ȝ', '&#540;': 'Ȝ', '&E;': 'Ę',
           '&amp;': '&', '&lt;': '<', '&gt;': '>', '&#383;': 'ſ'}
EE_HTML_KEYS = "&ae;&d;&t;&e;&AE;&D;&T;&#541;&#540;&E;&amp;&lt;&gt;&#383;"
EE_HTML_VALS = "æðþęÆÐÞȝȜĘ&<>ſ"
DOE_SGML = {'&ae;': 'æ', '&d;': 'ð', '&t;': 'þ', '&e;': 'ę', '&AE;': 'Æ',
            '&D;': 'Ð', '&T;': 'Þ', '&E;': 'Ę', '&oe;': 'œ', '&amp;': '⁊',
            '&egrave;': 'è', '&eacute;': 'é', '&auml;': 'ä', '&ouml;': 'ö',
            '&uuml;': 'ü', '&amacron;': 'ā', '&cmacron;': 'c̄',
            '&emacron;': 'ē', '&imacron;': 'ī', '&nmacron;': 'n̄',
            '&omacron;': 'ō', '&pmacron;': 'p̄', '&qmacron;': 'q̄',
            '&rmacron;': 'r̄', '&lt;': '<', '&gt;': '>', '&lbar;': 'ł',
            '&tbar;': 'ꝥ', '&bbar;': 'ƀ'}
DOE_SGML_KEYS = "&ae;&d;&t;&e;&AE;&D;&T;&E;&oe;&amp;&egrave;&eacute;&auml;" \
                "&ouml;&uuml;&amacron;&cmacron;&emacron;&imacron;&nmacron;" \
                "&omacron;&pmacron;&qmacron;&rmacron;&lt;&gt;&lbar;&tbar;" \
                "&bbar;"
DOE_SGML_VALS = "æðþęÆÐÞĘœ⁊èéäöüāc̄ēīn̄ōp̄q̄r̄<>łꝥƀ"
MUFI3 = {'&aenl;': '\ueee0', '&ascap;': 'ᴀ', '&ordf;': 'ª', '&aogon;': 'ą',
         '&Aogon;': 'Ą', '&acurl;': '\ue433', '&Acurl;': '\ue033',
         '&adotbl;': 'ạ', '&Adotbl;': 'Ạ', '&adot;': 'ȧ', '&Adot;': 'Ȧ',
         '&auml;': 'ä', '&Auml;': 'Ä', '&adiaguml;': '\ue8d5',
         '&adotbluml;': '\ue41d', '&aacute;': 'á', '&Aacute;': 'Á',
         '&aenlacute;': '\ueaf0', '&aogonacute;': '\ue404',
         '&Aogonacute;': '\ue004', '&adblac;': '\ue425', '&Adblac;': '\ue025',
         '&adotacute;': '\uebf5', '&Adotacute;': '\uebf4', '&agrave;': 'à',
         '&Agrave;': 'À', '&acirc;': 'â', '&Acirc;': 'Â',
         '&aumlcirc;': '\ue41a', '&aringcirc;': '\ue41f', '&atilde;': 'ã',
         '&Atilde;': 'Ã', '&aring;': 'å', '&Aring;': 'Å', '&ahook;': 'ả',
         '&Ahook;': 'Ả', '&abreve;': 'ă', '&Abreve;': 'Ă', '&amacr;': 'ā',
         '&Amacr;': 'Ā', '&amacrbreve;': '\ue410', '&Amacrbreve;': '\ue010',
         '&abreveacute;': 'ắ', '&Abreveacute;': 'Ắ', '&amacracute;': '\ue40a',
         '&Amacracute;': '\ue00a', '&aalig;': 'ꜳ', '&aacloselig;': '\uefa0',
         '&AAlig;': 'Ꜳ', '&aaligenl;': '\uefdf', '&aaligdotbl;': '\ueff3',
         '&AAligdotbl;': '\ueff2', '&aaligdot;': '\uefef',
         '&AAligdot;': '\uefee', '&aaliguml;': '\uefff',
         '&AAliguml;': '\ueffe', '&aaligacute;': '\uefe1',
         '&AAligacute;': '\uefe0', '&aaligdblac;': '\uefeb',
         '&AAligdblac;': '\uefea', '&aelig;': 'æ', '&AElig;': 'Æ',
         '&aeligenl;': '\ueaf1', '&aeligscap;': 'ᴁ', '&aeligred;': '\uf204',
         '&aeligcurl;': '\uebeb', '&AEligcurl;': '\uebea',
         '&aeligogon;': '\ue440', '&AEligogon;': '\ue040',
         '&aeligdotbl;': '\ue436', '&AEligdotbl;': '\ue036',
         '&aeligdot;': '\ue443', '&AEligdot;': '\ue043',
         '&aeliguml;': '\ue442', '&AEliguml;': '\ue042', '&aeligacute;': 'ǽ',
         '&AEligacute;': 'Ǽ', '&aeligogonacute;': '\ue8d3',
         '&aeligdblac;': '\ue441', '&AEligdblac;': '\ue041',
         '&aeligring;': '\ue8d1', '&aeligbreve;': '\ue43f',
         '&AEligbreve;': '\ue03f', '&aeligmacr;': 'ǣ', '&AEligmacr;': 'Ǣ',
         '&aeligmacrbreve;': '\ue43d', '&AEligmacrbreve;': '\ue03d',
         '&aeligmacracute;': '\ue43a', '&AEligmacracute;': '\ue03a',
         '&aflig;': '\uefa3', '&afinslig;': '\uefa4', '&aglig;': '\uefa5',
         '&allig;': '\uefa6', '&anlig;': '\uefa7', '&anscaplig;': '\uefa8',
         '&aolig;': 'ꜵ', '&AOlig;': 'Ꜵ', '&aoligenl;': '\uefde',
         '&aenlosmalllig;': '\ueaf2', '&aoligred;': '\uf206',
         '&AOligred;': '\uf205', '&aoligdotbl;': '\ueff5',
         '&AOligdotbl;': '\ueff4', '&aoligacute;': '\uefe3',
         '&AOligacute;': '\uefe2', '&aoligdblac;': '\uebc1',
         '&AOligdblac;': '\uebc0', '&aplig;': '\uefa9', '&arlig;': '\uefaa',
         '&arscaplig;': '\uefab', '&aulig;': 'ꜷ', '&AUlig;': 'Ꜷ',
         '&auligdotbl;': '\ueff7', '&AUligdotbl;': '\ueff6',
         '&auligacute;': '\uefe5', '&AUligacute;': '\uefe4', '&avlig;': 'ꜹ',
         '&AVlig;': 'Ꜹ', '&avligslash;': 'ꜻ', '&AVligslash;': 'Ꜻ',
         '&avligslashacute;': '\uebb1', '&AVligslashacute;': '\uebb0',
         '&avligogon;': '\uebf1', '&AVligogon;': '\uebf0',
         '&avligdotbl;': '\ueff9', '&AVligdotbl;': '\ueff8',
         '&avligacute;': '\uefe7', '&AVligacute;': '\uefe6',
         '&avligdblac;': '\uebc3', '&AVligdblac;': '\uebc2', '&aylig;': 'ꜽ',
         '&AYlig;': 'Ꜽ', '&ayligdotbl;': '\ueffb', '&AYligdotbl;': '\ueffa',
         '&ayligdot;': '\ueff1', '&AYligdot;': '\ueff0',
         '&athornlig;': '\uefac', '&aesup;': '\ue42c', '&Aesup;': '\ue02c',
         '&iesup;': '\ue54a', '&aosup;': '\ue42d', '&ausup;': '\ue8e1',
         '&avsup;': '\ue42e', '&aunc;': '\uf214', '&aopen;': '\uf202',
         '&ains;': '\uf200', '&Ains;': '\uf201', '&aneckless;': '\uf215',
         '&anecklesselig;': '\uefa1', '&AnecklessElig;': '\uefae',
         '&anecklessvlig;': '\uefa2', '&aclose;': '\uf203', '&Asqu;': '\uf13a',
         '&benl;': '\ueee1', '&bscap;': 'ʙ', '&bscapdot;': '\uebd0',
         '&bscapdotbl;': '\uef25', '&bdotbl;': 'ḅ', '&Bdotbl;': 'Ḅ',
         '&bdot;': 'ḃ', '&Bdot;': 'Ḃ', '&bacute;': '\ue444',
         '&Bacute;': '\ue044', '&bstrok;': 'ƀ', '&bovlmed;': '\ue44d',
         '&bblig;': '\ueec2', '&bglig;': '\ueec3', '&cenl;': '\ueee2',
         '&cscap;': 'ᴄ', '&ccedil;': 'ç', '&Ccedil;': 'Ç', '&cogon;': '\ue476',
         '&Cogon;': '\ue076', '&cdotbl;': '\ue466', '&Cdotbl;': '\ue066',
         '&cdot;': 'ċ', '&Cdot;': 'Ċ', '&cacute;': 'ć', '&Cacute;': 'Ć',
         '&Covlhigh;': '\uf7b5', '&cklig;': '\ueec4', '&ctlig;': '\ueec5',
         '&Csqu;': '\uf106', '&ccurl;': '\uf198', '&CONbase;': 'Ↄ',
         '&conbase;': 'ↄ', '&denl;': '\ueee3', '&dscap;': 'ᴅ', '&dstrok;': 'đ',
         '&Dstrok;': 'Đ', '&dovlmed;': '\ue491', '&dtailstrok;': 'ꝱ',
         '&dtail;': 'ɖ', '&dscapdot;': '\uebd2', '&ddotbl;': 'ḍ',
         '&Ddotbl;': 'Ḍ', '&dscapdotbl;': '\uef26', '&ddot;': 'ḋ',
         '&Ddot;': 'Ḋ', '&dacute;': '\ue477', '&Dacute;': '\ue077',
         '&eth;': 'ð', '&ETH;': 'Ð', '&ethenl;': '\ueee5', '&ethscap;': 'ᴆ',
         '&ethdotbl;': '\ue48f', '&ETHdotbl;': '\ue08f',
         '&Dovlhigh;': '\uf7b6', '&drotdrotlig;': '\ueec6', '&Drot;': 'Ꝺ',
         '&drot;': 'ꝺ', '&drotdot;': '\uebd1', '&drotacute;': '\uebb2',
         '&drotenl;': '\ueee4', '&dscript;': 'ẟ', '&dcurl;': '\uf193',
         '&eenl;': '\ueee6', '&escap;': 'ᴇ', '&eogon;': 'ę', '&Eogon;': 'Ę',
         '&ecurl;': '\ue4e9', '&Ecurl;': '\ue0e9', '&eogoncurl;': '\uebf3',
         '&Eogoncurl;': '\uebf2', '&edotbl;': 'ẹ', '&Edotbl;': 'Ẹ',
         '&eogondot;': '\ue4eb', '&Eogondot;': '\ue0eb',
         '&eogondotbl;': '\ue4e8', '&Eogondotbl;': '\ue0e8',
         '&eogonenl;': '\ueaf3', '&edot;': 'ė', '&Edot;': 'Ė', '&euml;': 'ë',
         '&Euml;': 'Ë', '&eumlmacr;': '\ue4cd', '&eacute;': 'é',
         '&Eacute;': 'É', '&eogonacute;': '\ue499', '&Eogonacute;': '\ue099',
         '&edotblacute;': '\ue498', '&edblac;': '\ue4d1', '&Edblac;': '\ue0d1',
         '&edotacute;': '\ue4c8', '&Edotacute;': '\ue0c8',
         '&eogondotacute;': '\ue4ec', '&Eogondotacute;': '\ue0ec',
         '&eogondblac;': '\ue4ea', '&Eogondblac;': '\ue0ea', '&egrave;': 'è',
         '&Egrave;': 'È', '&ecirc;': 'ê', '&Ecirc;': 'Ê',
         '&eogoncirc;': '\ue49f', '&ering;': '\ue4cf', '&ebreve;': 'ĕ',
         '&Ebreve;': 'Ĕ', '&emacr;': 'ē', '&Emacr;': 'Ē',
         '&eogonmacr;': '\ue4bc', '&Eogonmacr;': '\ue0bc',
         '&emacrbreve;': '\ue4b7', '&Emacrbreve;': '\ue0b7',
         '&emacracute;': 'ḗ', '&Emacracute;': 'Ḗ', '&eylig;': '\ueec7',
         '&eacombcirc;': '\uebbd', '&eucombcirc;': '\uebbe',
         '&easup;': '\ue4e1', '&Easup;': '\ue0e1', '&eesup;': '\ue8e2',
         '&eisup;': '\ue4e2', '&eosup;': '\ue8e3', '&evsup;': '\ue4e3',
         '&schwa;': 'ə', '&Eunc;': '\uf10a', '&Euncclose;': '\uf217',
         '&eunc;': '\uf218', '&eext;': '\uf219', '&etall;': '\uf21a',
         '&fenl;': '\ueee7', '&fscap;': 'ꜰ', '&fdotbl;': '\ue4ee',
         '&Fdotbl;': '\ue0ee', '&fdot;': 'ḟ', '&Fdot;': 'Ḟ',
         '&fscapdot;': '\uebd7', '&facute;': '\ue4f0', '&Facute;': '\ue0f0',
         '&faumllig;': '\ueec8', '&fflig;': 'ﬀ', '&filig;': 'ﬁ',
         '&fjlig;': '\ueec9', '&foumllig;': '\uf1bc', '&fllig;': 'ﬂ',
         '&frlig;': '\ueeca', '&ftlig;': '\ueecb', '&fuumllig;': '\ueecc',
         '&fylig;': '\ueecd', '&ffilig;': 'ﬃ', '&ffllig;': 'ﬄ',
         '&fftlig;': '\ueece', '&ffylig;': '\ueecf', '&ftylig;': '\ueed0',
         '&fturn;': 'ⅎ', '&Fturn;': 'Ⅎ', '&Frev;': 'ꟻ', '&fins;': 'ꝼ',
         '&Fins;': 'Ꝼ', '&finsenl;': '\ueeff', '&finsdot;': '\uebd4',
         '&Finsdot;': '\uebd3', '&finsdothook;': '\uf21c',
         '&finssemiclose;': '\uf21b', '&finssemiclosedot;': '\uebd5',
         '&finsclose;': '\uf207', '&finsclosedot;': '\uebd6',
         '&finsdotbl;': '\ue7e5', '&Finsdotbl;': '\ue3e5',
         '&finsacute;': '\uebb4', '&Finsacute;': '\uebb3', '&fcurl;': '\uf194',
         '&genl;': '\ueee8', '&gscap;': 'ɢ', '&gstrok;': 'ǥ', '&Gstrok;': 'Ǥ',
         '&gdotbl;': '\ue501', '&Gdotbl;': '\ue101', '&gscapdotbl;': '\uef27',
         '&gdot;': 'ġ', '&Gdot;': 'Ġ', '&gscapdot;': '\uef20', '&Gacute;': 'Ǵ',
         '&gacute;': 'ǵ', '&gglig;': '\ueed1', '&gdlig;': '\ueed2',
         '&gdrotlig;': '\ueed3', '&gethlig;': '\ueed4', '&golig;': '\ueede',
         '&gplig;': '\uead2', '&grlig;': '\uead0', '&gins;': 'ᵹ',
         '&Gins;': 'Ᵹ', '&ginsturn;': 'ꝿ', '&Ginsturn;': 'Ꝿ',
         '&Gsqu;': '\uf10e', '&gdivloop;': '\uf21d', '&glglowloop;': '\uf21e',
         '&gsmlowloop;': '\uf21f', '&gopen;': 'ɡ', '&gcurl;': '\uf196',
         '&henl;': '\ueee9', '&hscap;': 'ʜ', '&hhook;': 'ɦ', '&hstrok;': 'ħ',
         '&hovlmed;': '\ue517', '&hdotbl;': 'ḥ', '&Hdotbl;': 'Ḥ',
         '&Hdot;': 'ḣ', '&hdot;': 'Ḣ', '&hscapdot;': '\uebda',
         '&hacute;': '\ue516', '&Hacute;': '\ue116', '&hwair;': 'ƕ',
         '&HWAIR;': 'Ƕ', '&hslonglig;': '\uebad', '&hslongligbar;': '\ue7c7',
         '&hrarmlig;': '\ue8c3', '&Hrarmlig;': '\ue8c2', '&hhalf;': 'ⱶ',
         '&Hhalf;': 'Ⱶ', '&Hunc;': '\uf110', '&hrdes;': '\uf23a',
         '&ienl;': '\ueeea', '&iscap;': 'ɪ', '&inodot;': 'ı',
         '&inodotenl;': '\ueefd', '&Idot;': 'İ', '&istrok;': 'ɨ',
         '&iogon;': 'į', '&Iogon;': 'Į', '&icurl;': '\ue52a',
         '&Icurl;': '\ue12a', '&idotbl;': 'ị', '&Idotbl;': 'Ị',
         '&ibrevinvbl;': '\ue548', '&iuml;': 'ï', '&Iuml;': 'Ï',
         '&iacute;': 'í', '&Iacute;': 'Í', '&idblac;': '\ue543',
         '&Idblac;': '\ue143', '&idotacute;': '\uebf7',
         '&Idotacute;': '\uebf6', '&igrave;': 'ì', '&Igrave;': 'Ì',
         '&icirc;': 'î', '&Icirc;': 'Î', '&ihook;': 'ỉ', '&Ihook;': 'Ỉ',
         '&ibreve;': 'ĭ', '&Ibreve;': 'Ĭ', '&imacr;': 'ī', '&Imacr;': 'Ī',
         '&iovlmed;': '\ue550', '&Iovlhigh;': '\ue150',
         '&imacrbreve;': '\ue537', '&Imacrbreve;': '\ue137',
         '&imacracute;': '\ue535', '&Imacracute;': '\ue135', '&ijlig;': 'ĳ',
         '&IJlig;': 'Ĳ', '&iasup;': '\ue8e4', '&iosup;': '\ue8e5',
         '&iusup;': '\ue8e6', '&ivsup;': '\ue54b', '&ilong;': '\uf220',
         '&Ilong;': 'ꟾ', '&jenl;': '\ueeeb', '&jscap;': 'ᴊ', '&jnodot;': 'ȷ',
         '&jnodotenl;': '\ueefe', '&Jdot;': '\ue15c', '&jnodotstrok;': 'ɟ',
         '&jbar;': 'ɉ', '&Jbar;': 'Ɉ', '&jcurl;': '\ue563',
         '&Jcurl;': '\ue163', '&juml;': '\uebe3', '&Juml;': '\uebe2',
         '&jdotbl;': '\ue551', '&Jdotbl;': '\ue151', '&jacute;': '\ue553',
         '&Jacute;': '\ue153', '&jdblac;': '\ue562', '&Jdblac;': '\ue162',
         '&jmacrmed;': '\ue554', '&jovlmed;': '\ue552',
         '&Jmacrhigh;': '\ue154', '&Jovlhigh;': '\ue152', '&jesup;': '\ue8e7',
         '&kenl;': '\ueeec', '&kscap;': 'ᴋ', '&khook;': 'ƙ', '&kbar;': 'ꝁ',
         '&Kbar;': 'Ꝁ', '&kovlmed;': '\ue7c3', '&kstrleg;': 'ꝃ',
         '&Kstrleg;': 'Ꝃ', '&kstrascleg;': 'ꝅ', '&Kstrascleg;': 'Ꝅ',
         '&kdot;': '\ue568', '&Kdot;': '\ue168', '&kscapdot;': '\uebdb',
         '&kdotbl;': 'ḳ', '&Kdotbl;': 'Ḳ', '&kacute;': 'ḱ', '&Kacute;': 'Ḱ',
         '&kslonglig;': '\uebae', '&kslongligbar;': '\ue7c8',
         '&krarmlig;': '\ue8c5', '&kunc;': '\uf208', '&ksemiclose;': '\uf221',
         '&kclose;': '\uf209', '&kcurl;': '\uf195', '&lenl;': '\ueeed',
         '&lscap;': 'ʟ', '&lbar;': 'ƚ', '&lstrok;': 'ł', '&Lstrok;': 'Ł',
         '&lhighstrok;': 'ꝉ', '&Lhighstrok;': 'Ꝉ', '&lovlmed;': '\ue5b1',
         '&ltailstrok;': 'ꝲ', '&ldotbl;': 'ḷ', '&Ldotbl;': 'Ḷ',
         '&lscapdotbl;': '\uef28', '&ldot;': '\ue59e', '&Ldot;': '\ue19e',
         '&lscapdot;': '\uebdc', '&lacute;': 'ĺ', '&Lacute;': 'Ĺ',
         '&lringbl;': '\ue5a4', '&lmacrhigh;': '\ue596',
         '&lovlhigh;': '\ue58c', '&Lovlhigh;': '\uf7b4', '&lbrk;': 'ꝇ',
         '&Lbrk;': 'Ꝇ', '&llwelsh;': 'ỻ', '&LLwelsh;': 'Ỻ',
         '&lllig;': '\uf4f9', '&ldes;': '\uf222', '&lturn;': 'ꞁ',
         '&Lturn;': 'Ꞁ', '&menl;': '\ueeee', '&mscap;': 'ᴍ',
         '&mtailstrok;': 'ꝳ', '&mdotbl;': 'ṃ', '&Mdotbl;': 'Ṃ',
         '&mscapdotbl;': '\uef29', '&mdot;': 'ṁ', '&Mdot;': 'Ṁ',
         '&mscapdot;': '\uebdd', '&macute;': 'ḿ', '&Macute;': 'Ḿ',
         '&mringbl;': '\ue5c5', '&mmacrmed;': '\ue5b8',
         '&Mmacrhigh;': '\ue1b8', '&movlmed;': '\ue5d2',
         '&Movlhigh;': '\ue1d2', '&mesup;': '\ue8e8', '&Minv;': 'ꟽ',
         '&mrdes;': '\uf223', '&munc;': '\uf225', '&Munc;': '\uf11a',
         '&muncdes;': '\uf226', '&Muncdes;': '\uf224', '&muncacute;': '\uebb6',
         '&Muncacute;': '\uebb5', '&M5leg;': 'ꟿ', '&nenl;': '\ueeef',
         '&nscap;': 'ɴ', '&nscapldes;': '\uf22b', '&nlrleg;': 'ƞ',
         '&nlfhook;': 'ɲ', '&nbar;': '\ue7b2', '&ntailstrok;': 'ꝴ',
         '&ndot;': 'ṅ', '&Ndot;': 'Ṅ', '&nscapdot;': '\uef21', '&nacute;': 'ń',
         '&Nacute;': 'Ń', '&ndotbl;': 'ṇ', '&Ndotbl;': 'Ṇ',
         '&nscapdotbl;': '\uef2a', '&ncirc;': '\ue5d7', '&ntilde;': 'ñ',
         '&Ntilde;': 'Ñ', '&nringbl;': '\ue5ee', '&nmacrmed;': '\ue5dc',
         '&Nmacrhigh;': '\ue1dc', '&eng;': 'ŋ', '&ENG;': 'Ŋ',
         '&nscapslonglig;': '\ueed5', '&nrdes;': '\uf228', '&Nrdes;': '\uf229',
         '&nscaprdes;': '\uf22a', '&nflour;': '\uf19a', '&oenl;': '\ueef0',
         '&oscap;': 'ᴏ', '&ordm;': 'º', '&oogon;': 'ǫ', '&Oogon;': 'Ǫ',
         '&ocurl;': '\ue7d3', '&Ocurl;': '\ue3d3', '&oogoncurl;': '\ue64f',
         '&Oogoncurl;': '\ue24f', '&ocurlacute;': '\uebb8',
         '&Ocurlacute;': '\uebb7', '&oslash;': 'ø', '&Oslash;': 'Ø',
         '&oslashcurl;': '\ue7d4', '&Oslashcurl;': '\ue3d4',
         '&oslashogon;': '\ue655', '&Oslashogon;': '\ue255', '&odotbl;': 'ọ',
         '&Odotbl;': 'Ọ', '&oslashdotbl;': '\uebe1', '&Oslashdotbl;': '\uebe0',
         '&odot;': 'ȯ', '&Odot;': 'Ȯ', '&oogondot;': '\uebdf',
         '&Oogondot;': '\uebde', '&oogonmacr;': 'ǭ', '&Oogonmacr;': 'Ǭ',
         '&oslashdot;': '\uebce', '&Oslashdot;': '\uebcd',
         '&oogondotbl;': '\ue608', '&Oogondotbl;': '\ue208', '&ouml;': 'ö',
         '&Ouml;': 'Ö', '&odiaguml;': '\ue8d7', '&oumlacute;': '\ue62c',
         '&oacute;': 'ó', '&Oacute;': 'Ó', '&oslashacute;': 'ǿ',
         '&Oslashacute;': 'Ǿ', '&oslashdblac;': '\uebc7',
         '&Oslashdblac;': '\uebc6', '&oogonacute;': '\ue60c',
         '&Oogonacute;': '\ue20c', '&oslashogonacute;': '\ue657',
         '&Oslashogonacute;': '\ue257', '&odblac;': 'ő', '&Odblac;': 'Ő',
         '&odotacute;': '\uebf9', '&Odotacute;': '\uebf8',
         '&oogondotacute;': '\uebfb', '&Oogondotacute;': '\uebfa',
         '&oslashdotacute;': '\uebfd', '&Oslashdotacute;': '\uebfc',
         '&oogondblac;': '\uebc5', '&Oogondblac;': '\uebc4', '&ograve;': 'ò',
         '&Ograve;': 'Ò', '&ocirc;': 'ô', '&Ocirc;': 'Ô',
         '&oumlcirc;': '\ue62d', '&Oumlcirc;': '\ue22d',
         '&oogoncirc;': '\ue60e', '&ocar;': 'ǒ', '&Ocar;': 'Ǒ',
         '&otilde;': 'õ', '&Otilde;': 'Õ', '&oring;': '\ue637', '&ohook;': 'ỏ',
         '&Ohook;': 'Ỏ', '&obreve;': 'ŏ', '&Obreve;': 'Ŏ',
         '&oslashbreve;': '\uebef', '&Oslashbreve;': '\uebee', '&omacr;': 'ō',
         '&Omacr;': 'Ō', '&oslashmacr;': '\ue652', '&Oslashmacr;': '\ue252',
         '&omacrbreve;': '\ue61b', '&Omacrbreve;': '\ue21b',
         '&oslashmacrbreve;': '\ue653', '&Oslashmacrbreve;': '\ue253',
         '&omacracute;': 'ṓ', '&Omacracute;': 'Ṓ',
         '&oslashmacracute;': '\uebed', '&Oslashmacracute;': '\uebec',
         '&oumlmacr;': 'ȫ', '&Oumlmacr;': 'Ȫ', '&oclig;': '\uefad',
         '&oelig;': 'œ', '&OElig;': 'Œ', '&oeligscap;': 'ɶ',
         '&oeligenl;': '\uefdd', '&Oloop;': 'Ꝍ', '&oloop;': 'ꝍ',
         '&oeligacute;': '\ue659', '&OEligacute;': '\ue259',
         '&oeligdblac;': '\uebc9', '&OEligdblac;': '\uebc8',
         '&oeligmacr;': '\ue65d', '&OEligmacr;': '\ue25d',
         '&oeligmacrbreve;': '\ue660', '&OEligmacrbreve;': '\ue260',
         '&oolig;': 'ꝏ', '&OOlig;': 'Ꝏ', '&ooliguml;': '\uebe5',
         '&OOliguml;': '\uebe4', '&ooligacute;': '\uefe9',
         '&OOligacute;': '\uefe8', '&ooligdblac;': '\uefed',
         '&OOligdblac;': '\uefec', '&ooligdotbl;': '\ueffd',
         '&OOligdotbl;': '\ueffc', '&oasup;': '\ue643', '&oesup;': '\ue644',
         '&Oesup;': '\ue244', '&oisup;': '\ue645', '&oosup;': '\ue8e9',
         '&ousup;': '\ue646', '&Ousup;': '\ue246', '&ovsup;': '\ue647',
         '&oopen;': 'ɔ', '&oopenmacr;': '\ue7cc', '&penl;': '\ueef1',
         '&pscap;': 'ᴘ', '&pbardes;': 'ꝑ', '&Pbardes;': 'Ꝑ', '&pflour;': 'ꝓ',
         '&Pflour;': 'Ꝓ', '&psquirrel;': 'ꝕ', '&Psquirrel;': 'Ꝕ',
         '&pdotbl;': '\ue66d', '&Pdotbl;': '\ue26d', '&pdot;': 'ṗ',
         '&Pdot;': 'Ṗ', '&pscapdot;': '\uebcf', '&pacute;': 'ṕ',
         '&Pacute;': 'Ṕ', '&pmacr;': '\ue665', '&pplig;': '\ueed6',
         '&PPlig;': '\ueedd', '&ppflourlig;': '\ueed7', '&ppliguml;': '\uebe7',
         '&PPliguml;': '\uebe6', '&Prev;': 'ꟼ', '&qenl;': '\ueef2',
         '&qscap;': '\uef0c', '&qslstrok;': 'ꝙ', '&Qslstrok;': 'Ꝙ',
         '&qbardes;': 'ꝗ', '&Qbardes;': 'Ꝗ', '&qbardestilde;': '\ue68b',
         '&q2app;': '\ue8b3', '&q3app;': '\ue8bf', '&qcentrslstrok;': '\ue8b4',
         '&qdotbl;': '\ue688', '&Qdotbl;': '\ue288', '&qdot;': '\ue682',
         '&Qdot;': '\ue282', '&qmacr;': '\ue681', '&qvinslig;': '\uead1',
         '&Qstem;': '\uf22c', '&renl;': '\ueef3', '&rscap;': 'ʀ', '&YR;': 'Ʀ',
         '&rdes;': 'ɼ', '&rdesstrok;': '\ue7e4', '&rtailstrok;': 'ꝵ',
         '&rscaptailstrok;': 'ꝶ', '&Rtailstrok;': '℞', '&Rslstrok;': '℟',
         '&rdotbl;': 'ṛ', '&Rdotbl;': 'Ṛ', '&rdot;': 'ṙ', '&Rdot;': 'Ṙ',
         '&rscapdot;': '\uef22', '&racute;': 'ŕ', '&Racute;': 'Ŕ',
         '&rringbl;': '\ue6a3', '&rscapdotbl;': '\uef2b', '&resup;': '\ue8ea',
         '&rrot;': 'ꝛ', '&Rrot;': 'Ꝛ', '&rrotdotbl;': '\ue7c1',
         '&rrotacute;': '\uebb9', '&rins;': 'ꞃ', '&Rins;': 'Ꞃ',
         '&rflour;': '\uf19b', '&senl;': '\ueef4', '&sscap;': 'ꜱ',
         '&sdot;': 'ṡ', '&Sdot;': 'Ṡ', '&sscapdot;': '\uef23', '&sacute;': 'ś',
         '&Sacute;': 'Ś', '&sdotbl;': 'ṣ', '&Sdotbl;': 'Ṣ',
         '&sscapdotbl;': '\uef2c', '&szlig;': 'ß', '&SZlig;': 'ẞ',
         '&slongaumllig;': '\ueba0', '&slongchlig;': '\uf4fa',
         '&slonghlig;': '\ueba1', '&slongilig;': '\ueba2',
         '&slongjlig;': '\uf4fb', '&slongklig;': '\uf4fc',
         '&slongllig;': '\ueba3', '&slongoumllig;': '\ueba4',
         '&slongplig;': '\ueba5', '&slongslig;': '\uf4fd',
         '&slongslonglig;': '\ueba6', '&slongslongilig;': '\ueba7',
         '&slongslongklig;': '\uf4fe', '&slongslongllig;': '\ueba8',
         '&slongslongtlig;': '\uf4ff', '&stlig;': 'ﬆ', '&slongtlig;': 'ﬅ',
         '&slongtilig;': '\ueba9', '&slongtrlig;': '\uebaa',
         '&slonguumllig;': '\uebab', '&slongvinslig;': '\uebac',
         '&slongdestlig;': '\ueada', '&slong;': 'ſ', '&slongenl;': '\ueedf',
         '&slongbarslash;': 'ẜ', '&slongbar;': 'ẝ', '&slongovlmed;': '\ue79e',
         '&slongslstrok;': '\ue8b8', '&slongflour;': '\ue8b7',
         '&slongacute;': '\uebaf', '&slongdes;': '\uf127',
         '&slongdotbl;': '\ue7c2', '&Sclose;': '\uf126', '&sclose;': '\uf128',
         '&sins;': 'ꞅ', '&Sins;': 'Ꞅ', '&tenl;': '\ueef5', '&tscap;': 'ᴛ',
         '&ttailstrok;': 'ꝷ', '&togon;': '\ue6ee', '&Togon;': '\ue2ee',
         '&tdotbl;': 'ṭ', '&Tdotbl;': 'Ṭ', '&tdot;': 'ṫ', '&Tdot;': 'Ṫ',
         '&tscapdot;': '\uef24', '&tscapdotbl;': '\uef2d',
         '&tacute;': '\ue6e2', '&Tacute;': '\ue2e2', '&trlig;': '\ueed8',
         '&ttlig;': '\ueed9', '&trottrotlig;': '\ueeda', '&tylig;': '\ueedb',
         '&tzlig;': '\ueedc', '&trot;': 'ꞇ', '&Trot;': 'Ꞇ',
         '&tcurl;': '\uf199', '&uenl;': '\ueef7', '&uscap;': 'ᴜ',
         '&ubar;': 'ʉ', '&uogon;': 'ų', '&Uogon;': 'Ų', '&ucurl;': '\ue731',
         '&Ucurl;': '\ue331', '&udotbl;': 'ụ', '&Udotbl;': 'Ụ',
         '&ubrevinvbl;': '\ue727', '&udot;': '\ue715', '&Udot;': '\ue315',
         '&uuml;': 'ü', '&Uuml;': 'Ü', '&uacute;': 'ú', '&Uacute;': 'Ú',
         '&udblac;': 'ű', '&Udblac;': 'Ű', '&udotacute;': '\uebff',
         '&Udotacute;': '\uebfe', '&ugrave;': 'ù', '&Ugrave;': 'Ù',
         '&uvertline;': '\ue724', '&Uvertline;': '\ue324', '&ucirc;': 'û',
         '&Ucirc;': 'Û', '&uumlcirc;': '\ue717', '&Uumlcirc;': '\ue317',
         '&ucar;': 'ǔ', '&Ucar;': 'Ǔ', '&uring;': 'ů', '&Uring;': 'Ů',
         '&uhook;': 'ủ', '&Uhook;': 'Ủ', '&ucurlbar;': '\uebbf',
         '&ubreve;': 'ŭ', '&Ubreve;': 'Ŭ', '&umacr;': 'ū', '&Umacr;': 'Ū',
         '&umacrbreve;': '\ue70b', '&Umacrbreve;': '\ue30b',
         '&umacracute;': '\ue709', '&Umacracute;': '\ue309', '&uumlmacr;': 'ǖ',
         '&Uumlmacr;': 'Ǖ', '&uasup;': '\ue8eb', '&uesup;': '\ue72b',
         '&Uesup;': '\ue32b', '&uisup;': '\ue72c', '&uosup;': '\ue72d',
         '&Uosup;': '\ue32d', '&uvsup;': '\ue8ec', '&uwsup;': '\ue8ed',
         '&venl;': '\ueef8', '&vscap;': 'ᴠ', '&vbar;': '\ue74e',
         '&vslash;': '\ue8ba', '&vdiagstrok;': 'ꝟ', '&Vdiagstrok;': 'Ꝟ',
         '&Vslstrok;': '℣', '&vdotbl;': 'ṿ', '&Vdotbl;': 'Ṿ',
         '&vdot;': '\ue74c', '&Vdot;': '\ue34c', '&vuml;': '\ue742',
         '&Vuml;': '\ue342', '&vacute;': '\ue73a', '&Vacute;': '\ue33a',
         '&vdblac;': '\ue74b', '&Vdblac;': '\ue34b', '&vcirc;': '\ue73b',
         '&Vcirc;': '\ue33b', '&vring;': '\ue743', '&vmacr;': '\ue74d',
         '&Vmacr;': '\ue34d', '&Vovlhigh;': '\uf7b2', '&wynn;': 'ƿ',
         '&WYNN;': 'Ƿ', '&vins;': 'ꝩ', '&Vins;': 'Ꝩ', '&vinsdotbl;': '\ue7e6',
         '&Vinsdotbl;': '\ue3e6', '&vinsdot;': '\ue7e7', '&Vinsdot;': '\ue3e7',
         '&vinsacute;': '\uebbb', '&Vinsacute;': '\uebba', '&vwelsh;': 'ỽ',
         '&Vwelsh;': 'Ỽ', '&wenl;': '\ueef9', '&wscap;': 'ᴡ', '&wdotbl;': 'ẉ',
         '&Wdotbl;': 'Ẉ', '&wdot;': 'ẇ', '&Wdot;': 'Ẇ', '&wuml;': 'ẅ',
         '&Wuml;': 'Ẅ', '&wacute;': 'ẃ', '&Wacute;': 'Ẃ', '&wdblac;': '\ue750',
         '&Wdblac;': '\ue350', '&wgrave;': 'ẁ', '&Wgrave;': 'Ẁ',
         '&wcirc;': 'ŵ', '&Wcirc;': 'Ŵ', '&wring;': 'ẘ', '&wmacr;': '\ue757',
         '&Wmacr;': '\ue357', '&wasup;': '\ue8f0', '&wesup;': '\ue753',
         '&Wesup;': '\ue353', '&wisup;': '\ue8f1', '&wosup;': '\ue754',
         '&wusup;': '\ue8f2', '&wvsup;': '\ue8f3', '&xenl;': '\ueefa',
         '&xscap;': '\uef11', '&xmod;': 'ˣ', '&xslashula;': '\ue8bd',
         '&xslashlra;': '\ue8be', '&Xovlhigh;': '\uf7b3', '&xldes;': '\uf232',
         '&yenl;': '\ueefb', '&yscap;': 'ʏ', '&ybar;': '\ue77b',
         '&ycurl;': '\ue785', '&Ycurl;': '\ue385', '&ydotbl;': 'ỵ',
         '&Ydotbl;': 'Ỵ', '&ydot;': 'ẏ', '&Ydot;': 'Ẏ', '&yuml;': 'ÿ',
         '&Yuml;': 'Ÿ', '&yacute;': 'ý', '&Yacute;': 'Ý', '&ydblac;': '\ue77c',
         '&Ydblac;': '\ue37c', '&ydotacute;': '\ue784',
         '&Ydotacute;': '\ue384', '&ygrave;': 'ỳ', '&Ygrave;': 'Ỳ',
         '&ycirc;': 'ŷ', '&Ycirc;': 'Ŷ', '&yring;': 'ẙ', '&yhook;': 'ỷ',
         '&Yhook;': 'Ỷ', '&ybreve;': '\ue776', '&Ybreve;': '\ue376',
         '&ymacr;': 'ȳ', '&Ymacr;': 'Ȳ', '&ymacrbreve;': '\ue775',
         '&Ymacrbreve;': '\ue375', '&ymacracute;': '\ue773',
         '&Ymacracute;': '\ue373', '&yylig;': 'ꝡ', '&YYlig;': 'Ꝡ',
         '&yyliguml;': '\uebe9', '&YYliguml;': '\uebe8',
         '&yyligdblac;': '\uebcb', '&YYligdblac;': '\uebca',
         '&yesup;': '\ue781', '&yrgmainstrok;': '\uf233', '&yloop;': 'ỿ',
         '&Yloop;': 'Ỿ', '&zenl;': '\ueefc', '&zscap;': 'ᴢ', '&zstrok;': 'ƶ',
         '&Zstrok;': 'Ƶ', '&zdotbl;': 'ẓ', '&Zdotbl;': 'Ẓ', '&zdot;': 'ż',
         '&Zdot;': 'Ż', '&zvisigot;': 'ꝣ', '&Zvisigot;': 'Ꝣ', '&ezh;': 'ʒ',
         '&EZH;': 'Ʒ', '&yogh;': 'ȝ', '&YOGH;': 'Ȝ', '&thorn;': 'þ',
         '&THORN;': 'Þ', '&thornenl;': '\ueef6', '&thornscap;': '\uef15',
         '&thornbar;': 'ꝥ', '&THORNbar;': 'Ꝥ', '&thornovlmed;': '\ue7a2',
         '&thornbarslash;': '\uf149', '&THORNbarslash;': '\ue337',
         '&thornbardes;': 'ꝧ', '&THORNbardes;': 'Ꝧ', '&thorndotbl;': '\ue79f',
         '&THORNdotbl;': '\ue39f', '&thornacute;': '\ue737',
         '&thornslonglig;': '\ue734', '&thornslongligbar;': '\ue735',
         '&thornrarmlig;': '\ue8c1', '&frac14;': '¼', '&frac12;': '½',
         '&frac34;': '¾', '&sup0;': '⁰', '&sup1;': '¹', '&sup2;': '²',
         '&sup3;': '³', '&sup4;': '⁴', '&sup5;': '⁵', '&sup6;': '⁶',
         '&sup7;': '⁷', '&sup8;': '⁸', '&sup9;': '⁹', '&sub0;': '₀',
         '&sub1;': '₁', '&sub2;': '₂', '&sub3;': '₃', '&sub4;': '₄',
         '&sub5;': '₅', '&sub6;': '₆', '&sub7;': '₇', '&sub8;': '₈',
         '&sub9;': '₉', '&romnumCDlig;': 'ↀ', '&romnumDDlig;': 'ↁ',
         '&romnumDDdbllig;': 'ↂ', '&romnumCrev;': 'Ↄ',
         '&romnumCrevovl;': '\uf23f', '&Imod;': 'ᴵ', '&Vmod;': '\uf1be',
         '&Xmod;': '\uf1bf', '&asup;': 'ͣ', '&aeligsup;': 'ᷔ',
         '&anligsup;': '\uf036', '&anscapligsup;': '\uf03a', '&aoligsup;': 'ᷕ',
         '&arligsup;': '\uf038', '&arscapligsup;': '\uf130', '&avligsup;': 'ᷖ',
         '&bsup;': '\uf012', '&bscapsup;': '\uf013', '&csup;': 'ͨ',
         '&ccedilsup;': 'ᷗ', '&dsup;': 'ͩ', '&drotsup;': 'ᷘ', '&ethsup;': 'ᷙ',
         '&dscapsup;': '\uf016', '&esup;': 'ͤ', '&eogonsup;': '\uf135',
         '&emacrsup;': '\uf136', '&fsup;': '\uf017', '&gsup;': 'ᷚ',
         '&gscapsup;': 'ᷛ', '&hsup;': 'ͪ', '&isup;': 'ͥ',
         '&inodotsup;': '\uf02f', '&jsup;': '\uf030', '&jnodotsup;': '\uf031',
         '&ksup;': 'ᷜ', '&kscapsup;': '\uf01c', '&lsup;': 'ᷝ',
         '&lscapsup;': 'ᷞ', '&msup;': 'ͫ', '&mscapsup;': 'ᷟ', '&nsup;': 'ᷠ',
         '&nscapsup;': 'ᷡ', '&osup;': 'ͦ', '&omacrsup;': '\uf13f',
         '&oslashsup;': '\uf032', '&oogonsup;': '\uf13e',
         '&orrotsup;': '\uf03e', '&orumsup;': '\uf03f', '&psup;': '\uf025',
         '&qsup;': '\uf033', '&rsup;': 'ͬ', '&rrotsup;': 'ᷣ',
         '&rumsup;': '\uf040', '&rscapsup;': 'ᷢ', '&ssup;': 'ᷤ',
         '&slongsup;': 'ᷥ', '&tsup;': 'ͭ', '&trotsup;': '\uf03b',
         '&tscapsup;': '\uf02a', '&usup;': 'ͧ', '&vsup;': 'ͮ',
         '&wsup;': '\uf03c', '&xsup;': 'ͯ', '&ysup;': '\uf02b', '&zsup;': 'ᷦ',
         '&thornsup;': '\uf03d', '&combgrave;': '̀', '&combacute;': '́',
         '&combcirc;': '̂', '&combcircdbl;': '᷍', '&combtilde;': '̃',
         '&combmacr;': '̄', '&combbreve;': '̆', '&combdot;': '̇',
         '&combuml;': '̈', '&combhook;': '̉', '&combring;': '̊',
         '&combdblac;': '̋', '&combsgvertl;': '̍', '&combdbvertl;': '̎',
         '&combdotbl;': '̣', '&combced;': '̧', '&dblbarbl;': '̳',
         '&dblovl;': '̿', '&combogon;': '̨', '&combastbl;': '͙',
         '&combdblbrevebl;': '͜', '&combtripbrevebl;': '\uf1fc',
         '&combcurl;': '᷎', '&combcurlhigh;': '\uf1c5',
         '&combdothigh;': '\uf1ca', '&combcurlbar;': '\uf1cc', '&bar;': '̅',
         '&macrhigh;': '\uf00a', '&macrmed;': '\uf00b', '&ovlhigh;': '\uf00c',
         '&ovlmed;': '\uf00d', '&barbl;': '̲', '&baracr;': '̶',
         '&arbar;': '\uf1c0', '&combcomma;': '̕', '&combtildevert;': '̾',
         '&er;': '͛', '&erang;': '\uf1c7', '&ercurl;': '\uf1c8',
         '&ersub;': '᷏', '&ra;': 'ᷓ', '&rabar;': '\uf1c1', '&urrot;': '\uf153',
         '&urlemn;': '\uf1c2', '&ur;': '᷑', '&us;': '᷒', '&combisbelow;': '᷐',
         '&period;': '.', '&semi;': ';', '&amp;': '&', '&Theta;': 'Θ',
         '&theta;': 'θ', '&obiit;': 'ꝋ', '&OBIIT;': 'Ꝋ', '&et;': '⁊',
         '&etslash;': '\uf158', '&ET;': '\uf142', '&ETslash;': '\uf1a7',
         '&apomod;': 'ʼ', '&esse;': '≈', '&est;': '∻', '&condes;': 'ꝯ',
         '&CONdes;': 'Ꝯ', '&condot;': 'ꜿ', '&CONdot;': 'Ꜿ',
         '&usbase;': '\uf1a6', '&USbase;': '\uf1a5', '&usmod;': 'ꝰ',
         '&rum;': 'ꝝ', '&RUM;': 'Ꝝ', '&de;': '\uf159', '&is;': 'ꝭ',
         '&IS;': 'Ꝭ', '&sstrok;': 'ꝸ', '&etfin;': 'ꝫ', '&ETfin;': 'Ꝫ',
         '&sem;': '\uf1ac', '&fMedrun;': 'ᚠ', '&mMedrun;': 'ᛘ', '&lbbar;': '℔',
         '&circ;': '^', '&acute;': '´', '&grave;': '`', '&uml;': '¨',
         '&tld;': '~', '&macr;': '¯', '&breve;': '˘', '&dot;': '˙',
         '&ring;': '˚', '&cedil;': '¸', '&ogon;': '˛', '&tilde;': '˜',
         '&dblac;': '˝', '&verbarup;': 'ˈ', '&middot;': '·',
         '&hyphpoint;': '‧', '&sgldr;': '․', '&dblldr;': '‥', '&hellip;': '…',
         '&colon;': ':', '&comma;': ',', '&tridotright;': '჻',
         '&tridotupw;': '∴', '&tridotdw;': '∵', '&quaddot;': '∷',
         '&lozengedot;': '⁘', '&midring;': '\uf1da', '&verbar;': '|',
         '&brvbar;': '¦', '&Verbar;': '‖', '&sol;': '/', '&fracsol;': '⁄',
         '&dblsol;': '⫽', '&bsol;': '\\', '&luslst;': '⸌', '&ruslst;': '⸍',
         '&rlslst;': '⸜', '&llslst;': '⸝', '&lowbar;': '_', '&hyphen;': '-',
         '&dash;': '‐', '&nbhy;': '‑', '&dbloblhyph;': '⸗', '&numdash;': '‒',
         '&ndash;': '–', '&mdash;': '—', '&horbar;': '―', '&excl;': '!',
         '&iexcl;': '¡', '&quest;': '?', '&iquest;': '¿', '&ramus;': '\uf1db',
         '&lpar;': '(', '&rpar;': ')', '&lUbrack;': '⸦', '&rUbrack;': '⸧',
         '&ldblpar;': '⸨', '&rdblpar;': '⸩', '&lsqb;': '[', '&rsqb;': ']',
         '&lcub;': '{', '&rcub;': '}', '&lsqbqu;': '⁅', '&rsqbqu;': '⁆',
         '&lwhsqb;': '⟦', '&rwhsqb;': '⟧', '&verbarql;': '⸡',
         '&verbarqr;': '⸠', '&luhsqb;': '⸢', '&ruhsqb;': '⸣', '&llhsqb;': '⸤',
         '&rlhsqb;': '⸥', '&apos;': "'", '&prime;': '′', '&quot;': '"',
         '&Prime;': '″', '&lsquo;': '‘', '&rsquo;': '’', '&lsquolow;': '‚',
         '&rsquorev;': '‛', '&ldquo;': '“', '&rdquo;': '”', '&ldquolow;': '„',
         '&rdquorev;': '‟', '&lsaquo;': '‹', '&laquo;': '«', '&lt;': '<',
         '&langb;': '⟨', '&rsaquo;': '›', '&gt;': '>', '&raquo;': '»',
         '&rangb;': '⟩', '&hidot;': '\uf1f8', '&posit;': '\uf1e2',
         '&ductsimpl;': '\uf1e3', '&punctvers;': '\uf1ea',
         '&punctposit;': '\uf1e4', '&colmidcomposit;': '\uf1e5',
         '&bidotscomposit;': '\uf1f2', '&tridotscomposit;': '\uf1e6',
         '&punctelev;': '\uf161', '&punctelevdiag;': '\uf1f0',
         '&punctelevhiback;': '\uf1fa', '&punctelevhack;': '\uf1fb',
         '&punctflex;': '\uf1f5', '&punctexclam;': '\uf1e7',
         '&punctinter;': '\uf160', '&punctintertilde;': '\uf1e8',
         '&punctinterlemn;': '\uf1f1', '&punctpercont;': '⸮',
         '&wavylin;': '\uf1f9', '&medcom;': '\uf1e0', '&parag;': '\uf1e1',
         '&renvoi;': '\uf1ec', '&tridotsdownw;': '⸪', '&tridotsupw;': '⸫',
         '&quaddots;': '⸬', '&fivedots;': '⸭', '&virgsusp;': '\uf1f4',
         '&virgmin;': '\uf1f7', '&dipledot;': '⋗', '&sp;': ' ',
         '&nbsp;': '\xa0', '&nnbsp;': '\u202f', '&enqd;': '\u2000',
         '&emqd;': '\u2001', '&ensp;': '\u2002', '&emsp;': '\u2003',
         '&emsp13;': '\u2004', '&emsp14;': '\u2005', '&emsp16;': '\u2006',
         '&numsp;': '\u2007', '&puncsp;': '\u2008', '&thinsp;': '\u2009',
         '&hairsp;': '\u200a', '&zerosp;': '\u200b', '&del;': '\x7f',
         '&shy;': '\xad', '&num;': '#', '&sect;': '§', '&ast;': '*',
         '&triast;': '⁂', '&commat;': '@', '&copy;': '©', '&reg;': '®',
         '&not;': '¬', '&logand;': '∧', '&para;': '¶', '&revpara;': '⁋',
         '&cross;': '✝', '&dagger;': '†', '&Dagger;': '‡', '&refmark;': '※',
         '&dotcross;': '⁜', '&hedera;': '❦', '&hederarot;': '❧',
         '&dollar;': '$', '&cent;': '¢', '&pound;': '£', '&curren;': '¤',
         '&yen;': '¥', '&pennygerm;': '₰', '&scruple;': '℈',
         '&romaslibr;': '\uf2e0', '&romXbar;': '\uf2e1',
         '&romscapxbar;': '\uf2e2', '&romscapybar;': '\uf2e3',
         '&romscapdslash;': '\uf2e4', '&drotbar;': '\uf159', '&ecu;': '\uf2e7',
         '&florloop;': '\uf2e8', '&grosch;': '\uf2e9', '&libradut;': '\uf2ea',
         '&librafren;': '\uf2eb', '&libraital;': '\uf2ec',
         '&libraflem;': '\uf2ed', '&liranuov;': '\uf2ee',
         '&lirasterl;': '\uf2ef', '&markold;': '\uf2f0',
         '&markflour;': '\uf2f1', '&msign;': '\uf2f2',
         '&msignflour;': '\uf2f3', '&penningar;': '\uf2f5',
         '&reichtalold;': '\uf2f6', '&schillgerm;': '\uf2f7',
         '&schillgermscript;': '\uf2f8', '&scudi;': '\uf2f9', '&ounce;': '℥',
         '&sestert;': '\uf2fa', '&romas;': '\uf2d8', '&romunc;': '\uf2d9',
         '&romsemunc;': '\uf2da', '&romsext;': '\uf2db',
         '&romdimsext;': '\uf2dc', '&romsiliq;': '\uf2dd',
         '&romquin;': '\uf2de', '&romdupond;': '\uf2df', '&plus;': '+',
         '&minus;': '−', '&plusmn;': '±', '&times;': '×', '&divide;': '÷',
         '&equals;': '=', '&infin;': '∞', '&notequals;': '≠', '&percnt;': '%',
         '&permil;': '‰', '&deg;': '°', '&smallzero;': '\uf1bd',
         '&micro;': 'µ', '&dram;': '\uf2e6', '&obol;': '\uf2f4',
         '&sextans;': '\uf2fb', '&ouncescript;': '\uf2fd', '&arrsgllw;': '←',
         '&arrsglupw;': '↑', '&arrsglrw;': '→', '&arrsgldw;': '↓',
         '&squareblsm;': '▪', '&squarewhsm;': '▫', '&bull;': '•',
         '&circledot;': '◌', '&tribull;': '‣', '&trirightwh;': '▹',
         '&trileftwh;': '◃', '&metrshort;': '⏑', '&metrshortlong;': '⏒',
         '&metrlongshort;': '⏓', '&metrdblshortlong;': '⏔',
         '&metranc;': '\uf70a', '&metrancACUTE;': '\uf70b',
         '&metrancdblac;': '\uf719', '&metrancgrave;': '\uf70c',
         '&metrancdblgrave;': '\uf71a', '&metrbreve;': '\uf701',
         '&metrbreveacute;': '\uf706', '&metrbrevedblac;': '\uf717',
         '&metrbrevegrave;': '\uf707', '&metrbrevedblgrave;': '\uf718',
         '&metrmacr;': '\uf700', '&metrmacracute;': '\uf704',
         '&metrmacrdblac;': '\uf715', '&metrmacrgrave;': '\uf705',
         '&metrmacrdblgrave;': '\uf716', '&metrmacrbreve;': '\uf702',
         '&metrbrevemacr;': '\uf703', '&metrmacrbreveacute;': '\uf708',
         '&metrmacrbrevegrave;': '\uf709', '&metrdblbrevemacr;': '\uf72e',
         '&metrdblbrevemacracute;': '\uf71b',
         '&metrdblbrevemacrdblac;': '\uf71c', '&metrpause;': '\uf714'}
MUFI3_KEYS = "&aenl;&ascap;&ordf;&aogon;&Aogon;&acurl;&Acurl;&adotbl;" \
             "&Adotbl;&adot;&Adot;&auml;&Auml;&adiaguml;&adotbluml;&aacute;" \
             "&Aacute;&aenlacute;&aogonacute;&Aogonacute;&adblac;&Adblac;" \
             "&adotacute;&Adotacute;&agrave;&Agrave;&acirc;&Acirc;&aumlcirc;" \
             "&aringcirc;&atilde;&Atilde;&aring;&Aring;&ahook;&Ahook;" \
             "&abreve;&Abreve;&amacr;&Amacr;&amacrbreve;&Amacrbreve;" \
             "&abreveacute;&Abreveacute;&amacracute;&Amacracute;&aalig;" \
             "&aacloselig;&AAlig;&aaligenl;&aaligdotbl;&AAligdotbl;" \
             "&aaligdot;&AAligdot;&aaliguml;&AAliguml;&aaligacute;" \
             "&AAligacute;&aaligdblac;&AAligdblac;&aelig;&AElig;&aeligenl;" \
             "&aeligscap;&aeligred;&aeligcurl;&AEligcurl;&aeligogon;" \
             "&AEligogon;&aeligdotbl;&AEligdotbl;&aeligdot;&AEligdot;" \
             "&aeliguml;&AEliguml;&aeligacute;&AEligacute;&aeligogonacute;" \
             "&aeligdblac;&AEligdblac;&aeligring;&aeligbreve;&AEligbreve;" \
             "&aeligmacr;&AEligmacr;&aeligmacrbreve;&AEligmacrbreve;" \
             "&aeligmacracute;&AEligmacracute;&aflig;&afinslig;&aglig;" \
             "&allig;&anlig;&anscaplig;&aolig;&AOlig;&aoligenl;" \
             "&aenlosmalllig;&aoligred;&AOligred;&aoligdotbl;&AOligdotbl;" \
             "&aoligacute;&AOligacute;&aoligdblac;&AOligdblac;&aplig;&arlig;" \
             "&arscaplig;&aulig;&AUlig;&auligdotbl;&AUligdotbl;&auligacute;" \
             "&AUligacute;&avlig;&AVlig;&avligslash;&AVligslash;" \
             "&avligslashacute;&AVligslashacute;&avligogon;&AVligogon;" \
             "&avligdotbl;&AVligdotbl;&avligacute;&AVligacute;&avligdblac;" \
             "&AVligdblac;&aylig;&AYlig;&ayligdotbl;&AYligdotbl;&ayligdot;" \
             "&AYligdot;&athornlig;&aesup;&Aesup;&iesup;&aosup;&ausup;" \
             "&avsup;&aunc;&aopen;&ains;&Ains;&aneckless;&anecklesselig;" \
             "&AnecklessElig;&anecklessvlig;&aclose;&Asqu;&benl;&bscap;" \
             "&bscapdot;&bscapdotbl;&bdotbl;&Bdotbl;&bdot;&Bdot;&bacute;" \
             "&Bacute;&bstrok;&bovlmed;&bblig;&bglig;&cenl;&cscap;&ccedil;" \
             "&Ccedil;&cogon;&Cogon;&cdotbl;&Cdotbl;&cdot;&Cdot;&cacute;" \
             "&Cacute;&Covlhigh;&cklig;&ctlig;&Csqu;&ccurl;&CONbase;" \
             "&conbase;&denl;&dscap;&dstrok;&Dstrok;&dovlmed;&dtailstrok;" \
             "&dtail;&dscapdot;&ddotbl;&Ddotbl;&dscapdotbl;&ddot;&Ddot;" \
             "&dacute;&Dacute;&eth;&ETH;&ethenl;&ethscap;&ethdotbl;" \
             "&ETHdotbl;&Dovlhigh;&drotdrotlig;&Drot;&drot;&drotdot;" \
             "&drotacute;&drotenl;&dscript;&dcurl;&eenl;&escap;&eogon;" \
             "&Eogon;&ecurl;&Ecurl;&eogoncurl;&Eogoncurl;&edotbl;&Edotbl;" \
             "&eogondot;&Eogondot;&eogondotbl;&Eogondotbl;&eogonenl;&edot;" \
             "&Edot;&euml;&Euml;&eumlmacr;&eacute;&Eacute;&eogonacute;" \
             "&Eogonacute;&edotblacute;&edblac;&Edblac;&edotacute;" \
             "&Edotacute;&eogondotacute;&Eogondotacute;&eogondblac;" \
             "&Eogondblac;&egrave;&Egrave;&ecirc;&Ecirc;&eogoncirc;&ering;" \
             "&ebreve;&Ebreve;&emacr;&Emacr;&eogonmacr;&Eogonmacr;" \
             "&emacrbreve;&Emacrbreve;&emacracute;&Emacracute;&eylig;" \
             "&eacombcirc;&eucombcirc;&easup;&Easup;&eesup;&eisup;&eosup;" \
             "&evsup;&schwa;&Eunc;&Euncclose;&eunc;&eext;&etall;&fenl;" \
             "&fscap;&fdotbl;&Fdotbl;&fdot;&Fdot;&fscapdot;&facute;&Facute;" \
             "&faumllig;&fflig;&filig;&fjlig;&foumllig;&fllig;&frlig;&ftlig;" \
             "&fuumllig;&fylig;&ffilig;&ffllig;&fftlig;&ffylig;&ftylig;" \
             "&fturn;&Fturn;&Frev;&fins;&Fins;&finsenl;&finsdot;&Finsdot;" \
             "&finsdothook;&finssemiclose;&finssemiclosedot;&finsclose;" \
             "&finsclosedot;&finsdotbl;&Finsdotbl;&finsacute;&Finsacute;" \
             "&fcurl;&genl;&gscap;&gstrok;&Gstrok;&gdotbl;&Gdotbl;" \
             "&gscapdotbl;&gdot;&Gdot;&gscapdot;&Gacute;&gacute;&gglig;" \
             "&gdlig;&gdrotlig;&gethlig;&golig;&gplig;&grlig;&gins;&Gins;" \
             "&ginsturn;&Ginsturn;&Gsqu;&gdivloop;&glglowloop;&gsmlowloop;" \
             "&gopen;&gcurl;&henl;&hscap;&hhook;&hstrok;&hovlmed;&hdotbl;" \
             "&Hdotbl;&Hdot;&hdot;&hscapdot;&hacute;&Hacute;&hwair;&HWAIR;" \
             "&hslonglig;&hslongligbar;&hrarmlig;&Hrarmlig;&hhalf;&Hhalf;" \
             "&Hunc;&hrdes;&ienl;&iscap;&inodot;&inodotenl;&Idot;&istrok;" \
             "&iogon;&Iogon;&icurl;&Icurl;&idotbl;&Idotbl;&ibrevinvbl;&iuml;" \
             "&Iuml;&iacute;&Iacute;&idblac;&Idblac;&idotacute;&Idotacute;" \
             "&igrave;&Igrave;&icirc;&Icirc;&ihook;&Ihook;&ibreve;&Ibreve;" \
             "&imacr;&Imacr;&iovlmed;&Iovlhigh;&imacrbreve;&Imacrbreve;" \
             "&imacracute;&Imacracute;&ijlig;&IJlig;&iasup;&iosup;&iusup;" \
             "&ivsup;&ilong;&Ilong;&jenl;&jscap;&jnodot;&jnodotenl;&Jdot;" \
             "&jnodotstrok;&jbar;&Jbar;&jcurl;&Jcurl;&juml;&Juml;&jdotbl;" \
             "&Jdotbl;&jacute;&Jacute;&jdblac;&Jdblac;&jmacrmed;&jovlmed;" \
             "&Jmacrhigh;&Jovlhigh;&jesup;&kenl;&kscap;&khook;&kbar;&Kbar;" \
             "&kovlmed;&kstrleg;&Kstrleg;&kstrascleg;&Kstrascleg;&kdot;" \
             "&Kdot;&kscapdot;&kdotbl;&Kdotbl;&kacute;&Kacute;&kslonglig;" \
             "&kslongligbar;&krarmlig;&kunc;&ksemiclose;&kclose;&kcurl;" \
             "&lenl;&lscap;&lbar;&lstrok;&Lstrok;&lhighstrok;&Lhighstrok;" \
             "&lovlmed;&ltailstrok;&ldotbl;&Ldotbl;&lscapdotbl;&ldot;&Ldot;" \
             "&lscapdot;&lacute;&Lacute;&lringbl;&lmacrhigh;&lovlhigh;" \
             "&Lovlhigh;&lbrk;&Lbrk;&llwelsh;&LLwelsh;&lllig;&ldes;&lturn;" \
             "&Lturn;&menl;&mscap;&mtailstrok;&mdotbl;&Mdotbl;&mscapdotbl;" \
             "&mdot;&Mdot;&mscapdot;&macute;&Macute;&mringbl;&mmacrmed;" \
             "&Mmacrhigh;&movlmed;&Movlhigh;&mesup;&Minv;&mrdes;&munc;&Munc;" \
             "&muncdes;&Muncdes;&muncacute;&Muncacute;&M5leg;&nenl;&nscap;" \
             "&nscapldes;&nlrleg;&nlfhook;&nbar;&ntailstrok;&ndot;&Ndot;" \
             "&nscapdot;&nacute;&Nacute;&ndotbl;&Ndotbl;&nscapdotbl;&ncirc;" \
             "&ntilde;&Ntilde;&nringbl;&nmacrmed;&Nmacrhigh;&eng;&ENG;" \
             "&nscapslonglig;&nrdes;&Nrdes;&nscaprdes;&nflour;&oenl;&oscap;" \
             "&ordm;&oogon;&Oogon;&ocurl;&Ocurl;&oogoncurl;&Oogoncurl;" \
             "&ocurlacute;&Ocurlacute;&oslash;&Oslash;&oslashcurl;" \
             "&Oslashcurl;&oslashogon;&Oslashogon;&odotbl;&Odotbl;" \
             "&oslashdotbl;&Oslashdotbl;&odot;&Odot;&oogondot;&Oogondot;" \
             "&oogonmacr;&Oogonmacr;&oslashdot;&Oslashdot;&oogondotbl;" \
             "&Oogondotbl;&ouml;&Ouml;&odiaguml;&oumlacute;&oacute;&Oacute;" \
             "&oslashacute;&Oslashacute;&oslashdblac;&Oslashdblac;" \
             "&oogonacute;&Oogonacute;&oslashogonacute;&Oslashogonacute;" \
             "&odblac;&Odblac;&odotacute;&Odotacute;&oogondotacute;" \
             "&Oogondotacute;&oslashdotacute;&Oslashdotacute;&oogondblac;" \
             "&Oogondblac;&ograve;&Ograve;&ocirc;&Ocirc;&oumlcirc;&Oumlcirc;" \
             "&oogoncirc;&ocar;&Ocar;&otilde;&Otilde;&oring;&ohook;&Ohook;" \
             "&obreve;&Obreve;&oslashbreve;&Oslashbreve;&omacr;&Omacr;" \
             "&oslashmacr;&Oslashmacr;&omacrbreve;&Omacrbreve;" \
             "&oslashmacrbreve;&Oslashmacrbreve;&omacracute;&Omacracute;" \
             "&oslashmacracute;&Oslashmacracute;&oumlmacr;&Oumlmacr;&oclig;" \
             "&oelig;&OElig;&oeligscap;&oeligenl;&Oloop;&oloop;&oeligacute;" \
             "&OEligacute;&oeligdblac;&OEligdblac;&oeligmacr;&OEligmacr;" \
             "&oeligmacrbreve;&OEligmacrbreve;&oolig;&OOlig;&ooliguml;" \
             "&OOliguml;&ooligacute;&OOligacute;&ooligdblac;&OOligdblac;" \
             "&ooligdotbl;&OOligdotbl;&oasup;&oesup;&Oesup;&oisup;&oosup;" \
             "&ousup;&Ousup;&ovsup;&oopen;&oopenmacr;&penl;&pscap;&pbardes;" \
             "&Pbardes;&pflour;&Pflour;&psquirrel;&Psquirrel;&pdotbl;" \
             "&Pdotbl;&pdot;&Pdot;&pscapdot;&pacute;&Pacute;&pmacr;&pplig;" \
             "&PPlig;&ppflourlig;&ppliguml;&PPliguml;&Prev;&qenl;&qscap;" \
             "&qslstrok;&Qslstrok;&qbardes;&Qbardes;&qbardestilde;&q2app;" \
             "&q3app;&qcentrslstrok;&qdotbl;&Qdotbl;&qdot;&Qdot;&qmacr;" \
             "&qvinslig;&Qstem;&renl;&rscap;&YR;&rdes;&rdesstrok;" \
             "&rtailstrok;&rscaptailstrok;&Rtailstrok;&Rslstrok;&rdotbl;" \
             "&Rdotbl;&rdot;&Rdot;&rscapdot;&racute;&Racute;&rringbl;" \
             "&rscapdotbl;&resup;&rrot;&Rrot;&rrotdotbl;&rrotacute;&rins;" \
             "&Rins;&rflour;&senl;&sscap;&sdot;&Sdot;&sscapdot;&sacute;" \
             "&Sacute;&sdotbl;&Sdotbl;&sscapdotbl;&szlig;&SZlig;" \
             "&slongaumllig;&slongchlig;&slonghlig;&slongilig;&slongjlig;" \
             "&slongklig;&slongllig;&slongoumllig;&slongplig;&slongslig;" \
             "&slongslonglig;&slongslongilig;&slongslongklig;" \
             "&slongslongllig;&slongslongtlig;&stlig;&slongtlig;&slongtilig;" \
             "&slongtrlig;&slonguumllig;&slongvinslig;&slongdestlig;" \
             "&slong;&slongenl;&slongbarslash;&slongbar;&slongovlmed;" \
             "&slongslstrok;&slongflour;&slongacute;&slongdes;&slongdotbl;" \
             "&Sclose;&sclose;&sins;&Sins;&tenl;&tscap;&ttailstrok;&togon;" \
             "&Togon;&tdotbl;&Tdotbl;&tdot;&Tdot;&tscapdot;&tscapdotbl;" \
             "&tacute;&Tacute;&trlig;&ttlig;&trottrotlig;&tylig;&tzlig;" \
             "&trot;&Trot;&tcurl;&uenl;&uscap;&ubar;&uogon;&Uogon;&ucurl;" \
             "&Ucurl;&udotbl;&Udotbl;&ubrevinvbl;&udot;&Udot;&uuml;&Uuml;" \
             "&uacute;&Uacute;&udblac;&Udblac;&udotacute;&Udotacute;&ugrave;" \
             "&Ugrave;&uvertline;&Uvertline;&ucirc;&Ucirc;&uumlcirc;" \
             "&Uumlcirc;&ucar;&Ucar;&uring;&Uring;&uhook;&Uhook;&ucurlbar;" \
             "&ubreve;&Ubreve;&umacr;&Umacr;&umacrbreve;&Umacrbreve;" \
             "&umacracute;&Umacracute;&uumlmacr;&Uumlmacr;&uasup;&uesup;" \
             "&Uesup;&uisup;&uosup;&Uosup;&uvsup;&uwsup;&venl;&vscap;&vbar;" \
             "&vslash;&vdiagstrok;&Vdiagstrok;&Vslstrok;&vdotbl;&Vdotbl;" \
             "&vdot;&Vdot;&vuml;&Vuml;&vacute;&Vacute;&vdblac;&Vdblac;" \
             "&vcirc;&Vcirc;&vring;&vmacr;&Vmacr;&Vovlhigh;&wynn;&WYNN;" \
             "&vins;&Vins;&vinsdotbl;&Vinsdotbl;&vinsdot;&Vinsdot;" \
             "&vinsacute;&Vinsacute;&vwelsh;&Vwelsh;&wenl;&wscap;&wdotbl;" \
             "&Wdotbl;&wdot;&Wdot;&wuml;&Wuml;&wacute;&Wacute;&wdblac;" \
             "&Wdblac;&wgrave;&Wgrave;&wcirc;&Wcirc;&wring;&wmacr;&Wmacr;" \
             "&wasup;&wesup;&Wesup;&wisup;&wosup;&wusup;&wvsup;&xenl;&xscap;" \
             "&xmod;&xslashula;&xslashlra;&Xovlhigh;&xldes;&yenl;&yscap;" \
             "&ybar;&ycurl;&Ycurl;&ydotbl;&Ydotbl;&ydot;&Ydot;&yuml;&Yuml;" \
             "&yacute;&Yacute;&ydblac;&Ydblac;&ydotacute;&Ydotacute;&ygrave;" \
             "&Ygrave;&ycirc;&Ycirc;&yring;&yhook;&Yhook;&ybreve;&Ybreve;" \
             "&ymacr;&Ymacr;&ymacrbreve;&Ymacrbreve;&ymacracute;&Ymacracute;" \
             "&yylig;&YYlig;&yyliguml;&YYliguml;&yyligdblac;&YYligdblac;" \
             "&yesup;&yrgmainstrok;&yloop;&Yloop;&zenl;&zscap;&zstrok;" \
             "&Zstrok;&zdotbl;&Zdotbl;&zdot;&Zdot;&zvisigot;&Zvisigot;&ezh;" \
             "&EZH;&yogh;&YOGH;&thorn;&THORN;&thornenl;&thornscap;&thornbar;" \
             "&THORNbar;&thornovlmed;&thornbarslash;&THORNbarslash;" \
             "&thornbardes;&THORNbardes;&thorndotbl;&THORNdotbl;&thornacute;" \
             "&thornslonglig;&thornslongligbar;&thornrarmlig;&frac14;" \
             "&frac12;&frac34;&sup0;&sup1;&sup2;&sup3;&sup4;&sup5;&sup6;" \
             "&sup7;&sup8;&sup9;&sub0;&sub1;&sub2;&sub3;&sub4;&sub5;&sub6;" \
             "&sub7;&sub8;&sub9;&romnumCDlig;&romnumDDlig;&romnumDDdbllig;" \
             "&romnumCrev;&romnumCrevovl;&Imod;&Vmod;&Xmod;&asup;&aeligsup;" \
             "&anligsup;&anscapligsup;&aoligsup;&arligsup;&arscapligsup;" \
             "&avligsup;&bsup;&bscapsup;&csup;&ccedilsup;&dsup;&drotsup;" \
             "&ethsup;&dscapsup;&esup;&eogonsup;&emacrsup;&fsup;&gsup;" \
             "&gscapsup;&hsup;&isup;&inodotsup;&jsup;&jnodotsup;&ksup;" \
             "&kscapsup;&lsup;&lscapsup;&msup;&mscapsup;&nsup;&nscapsup;" \
             "&osup;&omacrsup;&oslashsup;&oogonsup;&orrotsup;&orumsup;&psup;" \
             "&qsup;&rsup;&rrotsup;&rumsup;&rscapsup;&ssup;&slongsup;&tsup;" \
             "&trotsup;&tscapsup;&usup;&vsup;&wsup;&xsup;&ysup;&zsup;" \
             "&thornsup;&combgrave;&combacute;&combcirc;&combcircdbl;" \
             "&combtilde;&combmacr;&combbreve;&combdot;&combuml;&combhook;" \
             "&combring;&combdblac;&combsgvertl;&combdbvertl;&combdotbl;" \
             "&combced;&dblbarbl;&dblovl;&combogon;&combastbl;" \
             "&combdblbrevebl;&combtripbrevebl;&combcurl;&combcurlhigh;" \
             "&combdothigh;&combcurlbar;&bar;&macrhigh;&macrmed;&ovlhigh;" \
             "&ovlmed;&barbl;&baracr;&arbar;&combcomma;&combtildevert;&er;" \
             "&erang;&ercurl;&ersub;&ra;&rabar;&urrot;&urlemn;&ur;&us;" \
             "&combisbelow;&period;&semi;&amp;&Theta;&theta;&obiit;&OBIIT;" \
             "&et;&etslash;&ET;&ETslash;&apomod;&esse;&est;&condes;&CONdes;" \
             "&condot;&CONdot;&usbase;&USbase;&usmod;&rum;&RUM;&de;&is;&IS;" \
             "&sstrok;&etfin;&ETfin;&sem;&fMedrun;&mMedrun;&lbbar;&circ;" \
             "&acute;&grave;&uml;&tld;&macr;&breve;&dot;&ring;&cedil;&ogon;" \
             "&tilde;&dblac;&verbarup;&middot;&hyphpoint;&sgldr;&dblldr;" \
             "&hellip;&colon;&comma;&tridotright;&tridotupw;&tridotdw;" \
             "&quaddot;&lozengedot;&midring;&verbar;&brvbar;&Verbar;&sol;" \
             "&fracsol;&dblsol;&bsol;&luslst;&ruslst;&rlslst;&llslst;" \
             "&lowbar;&hyphen;&dash;&nbhy;&dbloblhyph;&numdash;&ndash;" \
             "&mdash;&horbar;&excl;&iexcl;&quest;&iquest;&ramus;&lpar;&rpar;" \
             "&lUbrack;&rUbrack;&ldblpar;&rdblpar;&lsqb;&rsqb;&lcub;&rcub;" \
             "&lsqbqu;&rsqbqu;&lwhsqb;&rwhsqb;&verbarql;&verbarqr;&luhsqb;" \
             "&ruhsqb;&llhsqb;&rlhsqb;&apos;&prime;&quot;&Prime;&lsquo;" \
             "&rsquo;&lsquolow;&rsquorev;&ldquo;&rdquo;&ldquolow;&rdquorev;" \
             "&lsaquo;&laquo;&lt;&langb;&rsaquo;&gt;&raquo;&rangb;&hidot;" \
             "&posit;&ductsimpl;&punctvers;&punctposit;&colmidcomposit;" \
             "&bidotscomposit;&tridotscomposit;&punctelev;&punctelevdiag;" \
             "&punctelevhiback;&punctelevhack;&punctflex;&punctexclam;" \
             "&punctinter;&punctintertilde;&punctinterlemn;&punctpercont;" \
             "&wavylin;&medcom;&parag;&renvoi;&tridotsdownw;&tridotsupw;" \
             "&quaddots;&fivedots;&virgsusp;&virgmin;&dipledot;&sp;&nbsp;" \
             "&nnbsp;&enqd;&emqd;&ensp;&emsp;&emsp13;&emsp14;&emsp16;&numsp;" \
             "&puncsp;&thinsp;&hairsp;&zerosp;&del;&shy;&num;&sect;&ast;" \
             "&triast;&commat;&copy;&reg;&not;&logand;&para;&revpara;&cross;" \
             "&dagger;&Dagger;&refmark;&dotcross;&hedera;&hederarot;&dollar;" \
             "&cent;&pound;&curren;&yen;&pennygerm;&scruple;&romaslibr;" \
             "&romXbar;&romscapxbar;&romscapybar;&romscapdslash;&drotbar;" \
             "&ecu;&florloop;&grosch;&libradut;&librafren;&libraital;" \
             "&libraflem;&liranuov;&lirasterl;&markold;&markflour;&msign;" \
             "&msignflour;&penningar;&reichtalold;&schillgerm;" \
             "&schillgermscript;&scudi;&ounce;&sestert;&romas;&romunc;" \
             "&romsemunc;&romsext;&romdimsext;&romsiliq;&romquin;&romdupond;" \
             "&plus;&minus;&plusmn;&times;&divide;&equals;&infin;&notequals;" \
             "&percnt;&permil;&deg;&smallzero;&micro;&dram;&obol;&sextans;" \
             "&ouncescript;&arrsgllw;&arrsglupw;&arrsglrw;&arrsgldw;" \
             "&squareblsm;&squarewhsm;&bull;&circledot;&tribull;&trirightwh;" \
             "&trileftwh;&metrshort;&metrshortlong;&metrlongshort;" \
             "&metrdblshortlong;&metranc;&metrancACUTE;&metrancdblac;" \
             "&metrancgrave;&metrancdblgrave;&metrbreve;&metrbreveacute;" \
             "&metrbrevedblac;&metrbrevegrave;&metrbrevedblgrave;&metrmacr;" \
             "&metrmacracute;&metrmacrdblac;&metrmacrgrave;" \
             "&metrmacrdblgrave;&metrmacrbreve;&metrbrevemacr;" \
             "&metrmacrbreveacute;&metrmacrbrevegrave;&metrdblbrevemacr;" \
             "&metrdblbrevemacracute;&metrdblbrevemacrdblac;&metrpause;"
MUFI3_VALS = "ᴀªąĄạẠȧȦäÄáÁàÀâÂãÃåÅảẢăĂāĀắẮꜳꜲ" \
             "æÆᴁǽǼǣǢ" \
             "ꜵꜴꜷꜶꜹꜸꜻꜺꜽꜼ" \
             "ʙḅḄḃḂƀᴄçÇċĊćĆ" \
             "ↃↄᴅđĐꝱɖḍḌḋḊðÐᴆꝹꝺẟᴇęĘẹẸė" \
             "ĖëËéÉèÈêÊĕĔēĒḗḖəꜰḟḞ" \
             "ﬀﬁﬂﬃﬄⅎℲꟻꝼꝻɢǥǤġĠǴǵ" \
             "ᵹꝽꝿꝾɡʜɦħḥḤḣḢƕǶⱶⱵɪıİɨįĮịỊïÏ" \
             "íÍìÌîÎỉỈĭĬīĪĳĲꟾᴊȷɟɉɈᴋƙ" \
             "ꝁꝀꝃꝂꝅꝄḳḲḱḰʟƚłŁꝉꝈꝲḷḶĺĹꝇꝆỻỺꞁꞀᴍꝳṃṂṁ" \
             "ṀḿḾꟽꟿɴƞɲꝴṅṄńŃṇṆñÑŋŊ" \
             "ᴏºǫǪøØọỌȯȮǭǬöÖóÓǿǾőŐ" \
             "òÒôÔǒǑõÕỏỎŏŎōŌṓṒȫȪœŒɶꝌꝍ" \
             "ꝏꝎɔᴘꝑꝐꝓꝒꝕꝔṗṖṕṔꟼꝙꝘꝗꝖ" \
             "ʀƦɼꝵꝶ℞℟ṛṚṙṘŕŔꝛꝚꞃꞂꜱṡṠśŚṣṢßẞ" \
             "ﬆﬅſẜẝꞅꞄᴛꝷṭṬṫṪ" \
             "ꞇꞆᴜʉųŲụỤüÜúÚűŰùÙûÛǔǓůŮủỦŭŬūŪǖǕ" \
             "ᴠꝟꝞ℣ṿṾƿǷꝩꝨỽỼᴡẉẈẇẆẅẄẃẂẁẀŵŴẘ" \
             "ˣʏỵỴẏẎÿŸýÝỳỲŷŶẙỷỶȳȲꝡꝠỿỾᴢ" \
             "ƶƵẓẒżŻꝣꝢʒƷȝȜþÞꝥꝤꝧꝦ¼½¾⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉ↀↁↂↃ" \
             "ᴵͣᷔᷕᷖͨᷗͩᷘᷙͤᷚᷛͪͥᷜᷝᷞͫᷟᷠᷡͦͬᷣᷢᷤᷥͭͧͮͯᷦ" \
             "̧̨̣̳͙̀́̂̃̄̆̇̈̉̊̋̍̎̿͜᷍᷎̅̶̲̾͛̕᷏ᷓ᷐᷑᷒.;&ΘθꝋꝊ⁊ʼ≈∻ꝯ" \
             "ꝮꜿꜾꝰꝝꝜꝭꝬꝸꝫꝪᚠᛘ℔^´`¨~¯˘˙˚¸˛˜˝ˈ·‧․‥…:,჻∴∵∷⁘|¦‖/⁄⫽\⸌⸍⸜⸝_-‐‑⸗‒" \
             "–—―!¡?¿()⸦⸧⸨⸩[]{}⁅⁆⟦⟧⸡⸠⸢⸣⸤⸥'′\"″‘’‚‛“”„‟‹«<⟨›>»⟩" \
             "⸮⸪⸫⸬⸭⋗              ​­#§*⁂@©®¬∧¶" \
             "⁋✝†‡※⁜❦❧$¢£¤¥₰℈℥" \
             "+−±×÷=∞≠%‰°µ←↑→↓▪▫•◌‣▹◃⏑⏒⏓⏔"
MUFI4 = {'&aenl;': '\ueee0', '&ascap;': 'ᴀ', '&ordf;': 'ª', '&aogon;': 'ą',
         '&Aogon;': 'Ą', '&acurl;': '\ue433', '&Acurl;': '\ue033',
         '&adotbl;': 'ạ', '&Adotbl;': 'Ạ', '&adot;': 'ȧ', '&Adot;': 'Ȧ',
         '&auml;': 'ä', '&Auml;': 'Ä', '&adiaguml;': '\ue8d5',
         '&adotbluml;': '\ue41d', '&aacute;': 'á', '&Aacute;': 'Á',
         '&aenlacute;': '\ueaf0', '&aogonacute;': '\ue404',
         '&Aogonacute;': '\ue004', '&adblac;': '\ue425', '&Adblac;': '\ue025',
         '&adotacute;': '\uebf5', '&Adotacute;': '\uebf4', '&agrave;': 'à',
         '&Agrave;': 'À', '&acirc;': 'â', '&Acirc;': 'Â',
         '&aumlcirc;': '\ue41a', '&aringcirc;': '\ue41f', '&atilde;': 'ã',
         '&Atilde;': 'Ã', '&aring;': 'å', '&Aring;': 'Å', '&ahook;': 'ả',
         '&Ahook;': 'Ả', '&abreve;': 'ă', '&Abreve;': 'Ă', '&amacr;': 'ā',
         '&Amacr;': 'Ā', '&amacrbreve;': '\ue410', '&Amacrbreve;': '\ue010',
         '&abreveacute;': 'ắ', '&Abreveacute;': 'Ắ', '&amacracute;': '\ue40a',
         '&Amacracute;': '\ue00a', '&aalig;': 'ꜳ', '&aacloselig;': '\uefa0',
         '&AAlig;': 'Ꜳ', '&aaligenl;': '\uefdf', '&aaligdotbl;': '\ueff3',
         '&AAligdotbl;': '\ueff2', '&aaligdot;': '\uefef',
         '&AAligdot;': '\uefee', '&aaliguml;': '\uefff',
         '&AAliguml;': '\ueffe', '&aaligacute;': '\uefe1',
         '&AAligacute;': '\uefe0', '&aaligdblac;': '\uefeb',
         '&AAligdblac;': '\uefea', '&aelig;': 'æ', '&AElig;': 'Æ',
         '&aeligenl;': '\ueaf1', '&aeligscap;': 'ᴁ', '&aeligred;': '\uf204',
         '&aeligcurl;': '\uebeb', '&AEligcurl;': '\uebea',
         '&aeligogon;': '\ue440', '&AEligogon;': '\ue040',
         '&aeligdotbl;': '\ue436', '&AEligdotbl;': '\ue036',
         '&aeligdot;': '\ue443', '&AEligdot;': '\ue043',
         '&aeliguml;': '\ue442', '&AEliguml;': '\ue042', '&aeligacute;': 'ǽ',
         '&AEligacute;': 'Ǽ', '&aeligogonacute;': '\ue8d3',
         '&aeligdblac;': '\ue441', '&AEligdblac;': '\ue041',
         '&aeligring;': '\ue8d1', '&aeligbreve;': '\ue43f',
         '&AEligbreve;': '\ue03f', '&aeligmacr;': 'ǣ', '&AEligmacr;': 'Ǣ',
         '&aeligmacrbreve;': '\ue43d', '&AEligmacrbreve;': '\ue03d',
         '&aeligmacracute;': '\ue43a', '&AEligmacracute;': '\ue03a',
         '&aeligdotacute;': '\uefdb', '&AEligdotacute;': '\uefdc',
         '&aflig;': '\uefa3', '&afinslig;': '\uefa4', '&aglig;': '\uefa5',
         '&allig;': '\uefa6', '&anlig;': '\uefa7', '&anscaplig;': '\uefa8',
         '&aolig;': 'ꜵ', '&AOlig;': 'Ꜵ', '&aoligenl;': '\uefde',
         '&aenlosmalllig;': '\ueaf2', '&aoligred;': '\uf206',
         '&AOligred;': '\uf205', '&aoligdotbl;': '\ueff5',
         '&AOligdotbl;': '\ueff4', '&aoligacute;': '\uefe3',
         '&AOligacute;': '\uefe2', '&aoligdblac;': '\uebc1',
         '&AOligdblac;': '\uebc0', '&aplig;': '\uefa9',
         '&arlig;': '\uefaa', '&arscaplig;': '\uefab', '&aulig;': 'ꜷ',
         '&AUlig;': 'Ꜷ', '&auligdotbl;': '\ueff7', '&AUligdotbl;': '\ueff6',
         '&auligacute;': '\uefe5', '&AUligacute;': '\uefe4', '&avlig;': 'ꜹ',
         '&AVlig;': 'Ꜹ', '&avligslash;': 'ꜻ', '&AVligslash;': 'Ꜻ',
         '&avligslashacute;': '\uebb1', '&AVligslashacute;': '\uebb0',
         '&avligogon;': '\uebf1', '&AVligogon;': '\uebf0',
         '&avligdotbl;': '\ueff9', '&AVligdotbl;': '\ueff8',
         '&avligacute;': '\uefe7', '&AVligacute;': '\uefe6',
         '&avligdblac;': '\uebc3', '&AVligdblac;': '\uebc2',
         '&aylig;': 'ꜽ', '&AYlig;': 'Ꜽ', '&ayligdotbl;': '\ueffb',
         '&AYligdotbl;': '\ueffa', '&ayligdot;': '\ueff1',
         '&AYligdot;': '\ueff0', '&athornlig;': '\uefac', '&aesup;': '\ue42c',
         '&Aesup;': '\ue02c', '&iesup;': '\ue54a', '&aosup;': '\ue42d',
         '&ausup;': '\ue8e1', '&avsup;': '\ue42e', '&aunc;': '\uf214',
         '&aopen;': '\uf202', '&ains;': '\uf200', '&Ains;': '\uf201',
         '&aneckless;': '\uf215', '&anecklesselig;': '\uefa1',
         '&AnecklessElig;': '\uefae', '&anecklessvlig;': '\uefa2',
         '&aclose;': '\uf203', '&Asqu;': '\uf13a', '&benl;': '\ueee1',
         '&bscap;': 'ʙ', '&bscapdot;': '\uebd0', '&bscapdotbl;': '\uef25',
         '&bdotbl;': 'ḅ', '&Bdotbl;': 'Ḅ', '&bdot;': 'ḃ', '&Bdot;': 'Ḃ',
         '&bacute;': '\ue444', '&Bacute;': '\ue044', '&bstrok;': 'ƀ',
         '&bovlmed;': '\ue44d', '&bblig;': '\ueec2', '&bglig;': '\ueec3',
         '&cenl;': '\ueee2', '&cscap;': 'ᴄ', '&ccedil;': 'ç', '&Ccedil;': 'Ç',
         '&cogon;': '\ue476', '&Cogon;': '\ue076', '&cdotbl;': '\ue466',
         '&Cdotbl;': '\ue066', '&cdot;': 'ċ', '&Cdot;': 'Ċ', '&cacute;': 'ć',
         '&Cacute;': 'Ć', '&Covlhigh;': '\uf7b5', '&chlig;': '\uf1bb',
         '&cklig;': '\ueec4', '&ctlig;': '\ueec5', '&Csqu;': '\uf106',
         '&ccurl;': '\uf198', '&CONbase;': 'Ↄ', '&conbase;': 'ↄ',
         '&denl;': '\ueee3', '&dscap;': 'ᴅ', '&dstrok;': 'đ', '&Dstrok;': 'Đ',
         '&dovlmed;': '\ue491', '&dtailstrok;': 'ꝱ', '&dtail;': 'ɖ',
         '&dscapdot;': '\uebd2', '&ddotbl;': 'ḍ', '&Ddotbl;': 'Ḍ',
         '&dscapdotbl;': '\uef26', '&ddot;': 'ḋ', '&Ddot;': 'Ḋ',
         '&dacute;': '\ue477', '&Dacute;': '\ue077', '&eth;': 'ð',
         '&ETH;': 'Ð', '&ethenl;': '\ueee5', '&ethscap;': 'ᴆ',
         '&ethdotbl;': '\ue48f', '&ETHdotbl;': '\ue08f',
         '&Dovlhigh;': '\uf7b6', '&drotdrotlig;': '\ueec6', '&Drot;': 'Ꝺ',
         '&drot;': 'ꝺ', '&drotdot;': '\uebd1', '&drotacute;': '\uebb2',
         '&drotenl;': '\ueee4', '&dscript;': 'ẟ', '&dcurl;': '\uf193',
         '&eenl;': '\ueee6', '&escap;': 'ᴇ', '&eogon;': 'ę', '&Eogon;': 'Ę',
         '&ecurl;': '\ue4e9', '&Ecurl;': '\ue0e9', '&eogoncurl;': '\uebf3',
         '&Eogoncurl;': '\uebf2', '&edotbl;': 'ẹ', '&Edotbl;': 'Ẹ',
         '&eogondot;': '\ue4eb', '&Eogondot;': '\ue0eb',
         '&eogondotbl;': '\ue4e8', '&Eogondotbl;': '\ue0e8',
         '&eogonenl;': '\ueaf3', '&edot;': 'ė', '&Edot;': 'Ė', '&euml;': 'ë',
         '&Euml;': 'Ë', '&eumlmacr;': '\ue4cd', '&eacute;': 'é',
         '&Eacute;': 'É', '&eogonacute;': '\ue499', '&Eogonacute;': '\ue099',
         '&edotblacute;': '\ue498', '&edblac;': '\ue4d1', '&Edblac;': '\ue0d1',
         '&edotacute;': '\ue4c8', '&Edotacute;': '\ue0c8',
         '&eogondotacute;': '\ue4ec', '&Eogondotacute;': '\ue0ec',
         '&eogondblac;': '\ue4ea', '&Eogondblac;': '\ue0ea', '&egrave;': 'è',
         '&Egrave;': 'È', '&ecirc;': 'ê', '&Ecirc;': 'Ê',
         '&eogoncirc;': '\ue49f', '&ering;': '\ue4cf', '&ebreve;': 'ĕ',
         '&Ebreve;': 'Ĕ', '&emacr;': 'ē', '&Emacr;': 'Ē',
         '&eogonmacr;': '\ue4bc', '&Eogonmacr;': '\ue0bc',
         '&emacrbreve;': '\ue4b7', '&Emacrbreve;': '\ue0b7',
         '&emacracute;': 'ḗ', '&Emacracute;': 'Ḗ', '&eylig;': '\ueec7',
         '&eacombcirc;': '\uebbd', '&eucombcirc;': '\uebbe',
         '&easup;': '\ue4e1', '&Easup;': '\ue0e1', '&eesup;': '\ue8e2',
         '&eisup;': '\ue4e2', '&eosup;': '\ue8e3', '&evsup;': '\ue4e3',
         '&schwa;': 'ə', '&Eunc;': '\uf10a', '&Euncclose;': '\uf217',
         '&eunc;': '\uf218', '&eext;': '\uf219', '&etall;': '\uf21a',
         '&fenl;': '\ueee7', '&fscap;': 'ꜰ', '&fdotbl;': '\ue4ee',
         '&Fdotbl;': '\ue0ee', '&fdot;': 'ḟ', '&Fdot;': 'Ḟ',
         '&fscapdot;': '\uebd7', '&facute;': '\ue4f0', '&Facute;': '\ue0f0',
         '&faumllig;': '\ueec8', '&fflig;': 'ﬀ', '&filig;': 'ﬁ',
         '&fjlig;': '\ueec9', '&foumllig;': '\uf1bc', '&fllig;': 'ﬂ',
         '&frlig;': '\ueeca', '&ftlig;': '\ueecb', '&fuumllig;': '\ueecc',
         '&fylig;': '\ueecd', '&ffilig;': 'ﬃ', '&ffllig;': 'ﬄ',
         '&fftlig;': '\ueece', '&ffylig;': '\ueecf', '&ftylig;': '\ueed0',
         '&fturn;': 'ⅎ', '&Fturn;': 'Ⅎ', '&Frev;': 'ꟻ', '&fins;': 'ꝼ',
         '&Fins;': 'Ꝼ', '&finsenl;': '\ueeff', '&finsdot;': '\uebd4',
         '&Finsdot;': '\uebd3', '&finsdothook;': '\uf21c',
         '&finssemiclose;': '\uf21b', '&finssemiclosedot;': '\uebd5',
         '&finsclose;': '\uf207', '&finsclosedot;': '\uebd6',
         '&finsdotbl;': '\ue7e5', '&Finsdotbl;': '\ue3e5',
         '&finsacute;': '\uebb4', '&Finsacute;': '\uebb3', '&fcurl;': '\uf194',
         '&genl;': '\ueee8', '&gscap;': 'ɢ', '&gstrok;': 'ǥ', '&Gstrok;': 'Ǥ',
         '&gdotbl;': '\ue501', '&Gdotbl;': '\ue101', '&gscapdotbl;': '\uef27',
         '&gdot;': 'ġ', '&Gdot;': 'Ġ', '&gscapdot;': '\uef20', '&Gacute;': 'Ǵ',
         '&gacute;': 'ǵ', '&gglig;': '\ueed1', '&gdlig;': '\ueed2',
         '&gdrotlig;': '\ueed3', '&gethlig;': '\ueed4', '&golig;': '\ueede',
         '&gplig;': '\uead2', '&grlig;': '\uead0', '&gins;': 'ᵹ',
         '&Gins;': 'Ᵹ', '&ginsturn;': 'ꝿ', '&Ginsturn;': 'Ꝿ',
         '&Gsqu;': '\uf10e', '&gdivloop;': '\uf21d', '&glglowloop;': '\uf21e',
         '&gsmlowloop;': '\uf21f', '&gopen;': 'ɡ', '&gcurl;': '\uf196',
         '&henl;': '\ueee9', '&hscap;': 'ʜ', '&hhook;': 'ɦ', '&hstrok;': 'ħ',
         '&hovlmed;': '\ue517', '&hdotbl;': 'ḥ', '&Hdotbl;': 'Ḥ',
         '&Hdot;': 'ḣ', '&hdot;': 'Ḣ', '&hscapdot;': '\uebda',
         '&hacute;': '\ue516', '&Hacute;': '\ue116', '&hwair;': 'ƕ',
         '&HWAIR;': 'Ƕ', '&hslonglig;': '\uebad', '&hslongligbar;': '\ue7c7',
         '&hrarmlig;': '\ue8c3', '&Hrarmlig;': '\ue8c2', '&hhalf;': 'ⱶ',
         '&Hhalf;': 'Ⱶ', '&Hunc;': '\uf110', '&hrdes;': '\uf23a',
         '&ienl;': '\ueeea', '&iscap;': 'ɪ', '&inodot;': 'ı',
         '&inodotenl;': '\ueefd', '&Idot;': 'İ', '&istrok;': 'ɨ',
         '&idblstrok;': '\ue8a1', '&iogon;': 'į', '&inodotogon;': '\ue8dd',
         '&Iogon;': 'Į', '&icurl;': '\ue52a', '&Icurl;': '\ue12a',
         '&idotbl;': 'ị', '&Idotbl;': 'Ị', '&ibrevinvbl;': '\ue548',
         '&iuml;': 'ï', '&Iuml;': 'Ï', '&iacute;': 'í', '&Iacute;': 'Í',
         '&idblac;': '\ue543', '&Idblac;': '\ue143', '&idotacute;': '\uebf7',
         '&Idotacute;': '\uebf6', '&igrave;': 'ì', '&Igrave;': 'Ì',
         '&icirc;': 'î', '&Icirc;': 'Î', '&ihook;': 'ỉ', '&Ihook;': 'Ỉ',
         '&ibreve;': 'ĭ', '&Ibreve;': 'Ĭ', '&imacr;': 'ī', '&Imacr;': 'Ī',
         '&iovlmed;': '\ue550', '&Iovlhigh;': '\ue150',
         '&imacrbreve;': '\ue537', '&Imacrbreve;': '\ue137',
         '&imacracute;': '\ue535', '&Imacracute;': '\ue135', '&ijlig;': 'ĳ',
         '&IJlig;': 'Ĳ', '&iasup;': '\ue8e4', '&iosup;': '\ue8e5',
         '&iusup;': '\ue8e6', '&ivsup;': '\ue54b', '&ilong;': '\uf220',
         '&Ilong;': 'ꟾ', '&jenl;': '\ueeeb', '&jscap;': 'ᴊ', '&jnodot;': 'ȷ',
         '&jnodotenl;': '\ueefe', '&Jdot;': '\ue15c', '&jnodotstrok;': 'ɟ',
         '&jbar;': 'ɉ', '&jdblstrok;': '\ue8a2', '&Jbar;': 'Ɉ',
         '&jcurl;': '\ue563', '&Jcurl;': '\ue163', '&juml;': '\uebe3',
         '&Juml;': '\uebe2', '&jdotbl;': '\ue551', '&Jdotbl;': '\ue151',
         '&jacute;': '\ue553', '&Jacute;': '\ue153', '&jdblac;': '\ue562',
         '&Jdblac;': '\ue162', '&jmacrmed;': '\ue554', '&jovlmed;': '\ue552',
         '&Jmacrhigh;': '\ue154', '&Jovlhigh;': '\ue152', '&jesup;': '\ue8e7',
         '&kenl;': '\ueeec', '&kscap;': 'ᴋ', '&khook;': 'ƙ', '&kbar;': 'ꝁ',
         '&Kbar;': 'Ꝁ', '&kovlmed;': '\ue7c3', '&kstrleg;': 'ꝃ',
         '&Kstrleg;': 'Ꝃ', '&kstrascleg;': 'ꝅ', '&Kstrascleg;': 'Ꝅ',
         '&kdot;': '\ue568', '&Kdot;': '\ue168', '&kscapdot;': '\uebdb',
         '&kdotbl;': 'ḳ', '&Kdotbl;': 'Ḳ', '&kacute;': 'ḱ', '&Kacute;': 'Ḱ',
         '&kslonglig;': '\uebae', '&kslongligbar;': '\ue7c8',
         '&krarmlig;': '\ue8c5', '&kunc;': '\uf208', '&ksemiclose;': '\uf221',
         '&kclose;': '\uf209', '&kcurl;': '\uf195', '&lenl;': '\ueeed',
         '&lscap;': 'ʟ', '&lbar;': 'ƚ', '&lstrok;': 'ł', '&Lstrok;': 'Ł',
         '&lhighstrok;': 'ꝉ', '&Lhighstrok;': 'Ꝉ', '&lovlmed;': '\ue5b1',
         '&ltailstrok;': 'ꝲ', '&ldotbl;': 'ḷ', '&Ldotbl;': 'Ḷ',
         '&lscapdotbl;': '\uef28', '&ldot;': '\ue59e', '&Ldot;': '\ue19e',
         '&lscapdot;': '\uebdc', '&lacute;': 'ĺ', '&Lacute;': 'Ĺ',
         '&lringbl;': '\ue5a4', '&lmacrhigh;': '\ue596',
         '&lovlhigh;': '\ue58c', '&Lovlhigh;': '\uf7b4', '&lbrk;': 'ꝇ',
         '&Lbrk;': 'Ꝇ', '&llwelsh;': 'ỻ', '&LLwelsh;': 'Ỻ',
         '&lllig;': '\uf4f9', '&ldes;': '\uf222', '&lturn;': 'ꞁ',
         '&Lturn;': 'Ꞁ', '&menl;': '\ueeee', '&mscap;': 'ᴍ',
         '&mtailstrok;': 'ꝳ', '&mdotbl;': 'ṃ', '&Mdotbl;': 'Ṃ',
         '&mscapdotbl;': '\uef29', '&mdot;': 'ṁ', '&Mdot;': 'Ṁ',
         '&mscapdot;': '\uebdd', '&macute;': 'ḿ', '&Macute;': 'Ḿ',
         '&mringbl;': '\ue5c5', '&mmacrmed;': '\ue5b8',
         '&Mmacrhigh;': '\ue1b8', '&movlmed;': '\ue5d2',
         '&Movlhigh;': '\ue1d2', '&mesup;': '\ue8e8', '&Minv;': 'ꟽ',
         '&mturn;': 'ɯ', '&Mturn;': 'Ɯ', '&munc;': '\uf23c',
         '&mmedunc;': '\uf225', '&Munc;': '\uf11a', '&mrdes;': '\uf223',
         '&muncdes;': '\uf23d', '&mmeduncdes;': '\uf226',
         '&Muncdes;': '\uf224', '&muncacute;': '\uf23e',
         '&mmeduncacute;': '\uebb6', '&Muncacute;': '\uebb5', '&M5leg;': 'ꟿ',
         '&nenl;': '\ueeef', '&nscap;': 'ɴ', '&nscapldes;': '\uf22b',
         '&nlrleg;': 'ƞ', '&nlfhook;': 'ɲ', '&nbar;': '\ue7b2',
         '&ntailstrok;': 'ꝴ', '&ndot;': 'ṅ', '&Ndot;': 'Ṅ',
         '&nscapdot;': '\uef21', '&nacute;': 'ń', '&Nacute;': 'Ń',
         '&ndotbl;': 'ṇ', '&Ndotbl;': 'Ṇ', '&nscapdotbl;': '\uef2a',
         '&ncirc;': '\ue5d7', '&ntilde;': 'ñ', '&Ntilde;': 'Ñ',
         '&nringbl;': '\ue5ee', '&nmacrmed;': '\ue5dc',
         '&Nmacrhigh;': '\ue1dc', '&eng;': 'ŋ', '&ENG;': 'Ŋ',
         '&nscapslonglig;': '\ueed5', '&nrdes;': '\uf228', '&Nrdes;': '\uf229',
         '&nscaprdes;': '\uf22a', '&nflour;': '\uf19a', '&oenl;': '\ueef0',
         '&oscap;': 'ᴏ', '&ordm;': 'º', '&oogon;': 'ǫ', '&Oogon;': 'Ǫ',
         '&ocurl;': '\ue7d3', '&Ocurl;': '\ue3d3', '&oogoncurl;': '\ue64f',
         '&Oogoncurl;': '\ue24f', '&ocurlacute;': '\uebb8',
         '&Ocurlacute;': '\uebb7', '&oslash;': 'ø', '&Oslash;': 'Ø',
         '&oslashcurl;': '\ue7d4', '&Oslashcurl;': '\ue3d4',
         '&oslashogon;': '\ue655', '&Oslashogon;': '\ue255', '&odotbl;': 'ọ',
         '&Odotbl;': 'Ọ', '&oslashdotbl;': '\uebe1', '&Oslashdotbl;': '\uebe0',
         '&odot;': 'ȯ', '&Odot;': 'Ȯ', '&oogondot;': '\uebdf',
         '&Oogondot;': '\uebde', '&oogonmacr;': 'ǭ', '&Oogonmacr;': 'Ǭ',
         '&oslashdot;': '\uebce', '&Oslashdot;': '\uebcd',
         '&oogondotbl;': '\ue608', '&Oogondotbl;': '\ue208', '&ouml;': 'ö',
         '&Ouml;': 'Ö', '&odiaguml;': '\ue8d7', '&oumlacute;': '\ue62c',
         '&oacute;': 'ó', '&Oacute;': 'Ó', '&oslashacute;': 'ǿ',
         '&Oslashacute;': 'Ǿ', '&oslashdblac;': '\uebc7',
         '&Oslashdblac;': '\uebc6', '&oogonacute;': '\ue60c',
         '&Oogonacute;': '\ue20c', '&oslashogonacute;': '\ue657',
         '&Oslashogonacute;': '\ue257', '&odblac;': 'ő', '&Odblac;': 'Ő',
         '&odotacute;': '\uebf9', '&Odotacute;': '\uebf8',
         '&oogondotacute;': '\uebfb', '&Oogondotacute;': '\uebfa',
         '&oslashdotacute;': '\uebfd', '&Oslashdotacute;': '\uebfc',
         '&oogondblac;': '\uebc5', '&Oogondblac;': '\uebc4', '&ograve;': 'ò',
         '&Ograve;': 'Ò', '&ocirc;': 'ô', '&Ocirc;': 'Ô',
         '&oumlcirc;': '\ue62d', '&Oumlcirc;': '\ue22d',
         '&oogoncirc;': '\ue60e', '&ocar;': 'ǒ', '&Ocar;': 'Ǒ',
         '&otilde;': 'õ', '&Otilde;': 'Õ', '&oring;': '\ue637', '&ohook;': 'ỏ',
         '&Ohook;': 'Ỏ', '&obreve;': 'ŏ', '&Obreve;': 'Ŏ',
         '&oslashbreve;': '\uebef', '&Oslashbreve;': '\uebee', '&omacr;': 'ō',
         '&Omacr;': 'Ō', '&oslashmacr;': '\ue652', '&Oslashmacr;': '\ue252',
         '&omacrbreve;': '\ue61b', '&Omacrbreve;': '\ue21b',
         '&oslashmacrbreve;': '\ue653', '&Oslashmacrbreve;': '\ue253',
         '&omacracute;': 'ṓ', '&Omacracute;': 'Ṓ',
         '&oslashmacracute;': '\uebed', '&Oslashmacracute;': '\uebec',
         '&oumlmacr;': 'ȫ', '&Oumlmacr;': 'Ȫ', '&oclig;': '\uefad',
         '&oelig;': 'œ', '&OElig;': 'Œ', '&oeligscap;': 'ɶ',
         '&oeligenl;': '\uefdd', '&oeligogon;': '\ue662',
         '&OEligogon;': '\ue262', '&Oloop;': 'Ꝍ', '&oloop;': 'ꝍ',
         '&oeligacute;': '\ue659', '&OEligacute;': '\ue259',
         '&oeligdblac;': '\uebc9', '&OEligdblac;': '\uebc8',
         '&oeligmacr;': '\ue65d', '&OEligmacr;': '\ue25d',
         '&oeligmacrbreve;': '\ue660', '&OEligmacrbreve;': '\ue260',
         '&oolig;': 'ꝏ', '&OOlig;': 'Ꝏ', '&ooliguml;': '\uebe5',
         '&OOliguml;': '\uebe4', '&ooligacute;': '\uefe9',
         '&OOligacute;': '\uefe8', '&ooligdblac;': '\uefed',
         '&OOligdblac;': '\uefec', '&ooligdotbl;': '\ueffd',
         '&OOligdotbl;': '\ueffc', '&orrotlig;': '\ue8de', '&oasup;': '\ue643',
         '&oesup;': '\ue644', '&Oesup;': '\ue244', '&oisup;': '\ue645',
         '&oosup;': '\ue8e9', '&ousup;': '\ue646', '&Ousup;': '\ue246',
         '&ovsup;': '\ue647', '&oopen;': 'ɔ', '&oopenmacr;': '\ue7cc',
         '&penl;': '\ueef1', '&pscap;': 'ᴘ', '&pbardes;': 'ꝑ',
         '&Pbardes;': 'Ꝑ', '&pflour;': 'ꝓ', '&Pflour;': 'Ꝓ',
         '&psquirrel;': 'ꝕ', '&Psquirrel;': 'Ꝕ', '&pdotbl;': '\ue66d',
         '&Pdotbl;': '\ue26d', '&pdot;': 'ṗ', '&Pdot;': 'Ṗ',
         '&pscapdot;': '\uebcf', '&pacute;': 'ṕ', '&Pacute;': 'Ṕ',
         '&pdblac;': '\ue668', '&Pdblac;': '\ue268', '&pmacr;': '\ue665',
         '&pplig;': '\ueed6', '&PPlig;': '\ueedd', '&ppflourlig;': '\ueed7',
         '&ppliguml;': '\uebe7', '&PPliguml;': '\uebe6', '&Prev;': 'ꟼ',
         '&qenl;': '\ueef2', '&qscap;': '\uef0c', '&qslstrok;': 'ꝙ',
         '&Qslstrok;': 'Ꝙ', '&qbardes;': 'ꝗ', '&Qbardes;': 'Ꝗ',
         '&qbardestilde;': '\ue68b', '&q2app;': '\ue8b3', '&q3app;': '\ue8bf',
         '&qcentrslstrok;': '\ue8b4', '&qdotbl;': '\ue688',
         '&Qdotbl;': '\ue288', '&qdot;': '\ue682', '&Qdot;': '\ue282',
         '&qmacr;': '\ue681', '&qvinslig;': '\uead1', '&Qstem;': '\uf22c',
         '&renl;': '\ueef3', '&rscap;': 'ʀ', '&YR;': 'Ʀ', '&rdes;': 'ɼ',
         '&rdesstrok;': '\ue7e4', '&rtailstrok;': 'ꝵ', '&rscaptailstrok;': 'ꝶ',
         '&Rtailstrok;': '℞', '&Rslstrok;': '℟', '&rdotbl;': 'ṛ',
         '&Rdotbl;': 'Ṛ', '&rdot;': 'ṙ', '&Rdot;': 'Ṙ', '&rscapdot;': '\uef22',
         '&racute;': 'ŕ', '&Racute;': 'Ŕ', '&rringbl;': '\ue6a3',
         '&rscapdotbl;': '\uef2b', '&resup;': '\ue8ea', '&rrot;': 'ꝛ',
         '&Rrot;': 'Ꝛ', '&rrotdotbl;': '\ue7c1', '&rrotacute;': '\uebb9',
         '&rins;': 'ꞃ', '&Rins;': 'Ꞃ', '&rflour;': '\uf19b',
         '&senl;': '\ueef4', '&sscap;': 'ꜱ', '&sdot;': 'ṡ', '&Sdot;': 'Ṡ',
         '&sscapdot;': '\uef23', '&sacute;': 'ś', '&Sacute;': 'Ś',
         '&sdotbl;': 'ṣ', '&Sdotbl;': 'Ṣ', '&sscapdotbl;': '\uef2c',
         '&szlig;': 'ß', '&SZlig;': 'ẞ', '&slongaumllig;': '\ueba0',
         '&slongchlig;': '\uf4fa', '&slonghlig;': '\ueba1',
         '&slongilig;': '\ueba2', '&slongjlig;': '\uf4fb',
         '&slongklig;': '\uf4fc', '&slongllig;': '\ueba3',
         '&slonglbarlig;': '\ue8df', '&slongoumllig;': '\ueba4',
         '&slongplig;': '\ueba5', '&slongslig;': '\uf4fd',
         '&slongslonglig;': '\ueba6', '&slongslongilig;': '\ueba7',
         '&slongslongklig;': '\uf4fe', '&slongslongllig;': '\ueba8',
         '&slongslongtlig;': '\uf4ff', '&stlig;': 'ﬆ', '&slongtlig;': 'ﬅ',
         '&slongtilig;': '\ueba9', '&slongtrlig;': '\uebaa',
         '&slonguumllig;': '\uebab', '&slongvinslig;': '\uebac',
         '&slongdestlig;': '\ueada', '&slong;': 'ſ', '&slongenl;': '\ueedf',
         '&slongbarslash;': 'ẜ', '&slongbar;': 'ẝ', '&slongovlmed;': '\ue79e',
         '&slongslstrok;': '\ue8b8', '&slongflour;': '\ue8b7',
         '&slongacute;': '\uebaf', '&slongdes;': '\uf127',
         '&slongdotbl;': '\ue7c2', '&Sclose;': '\uf126', '&sclose;': '\uf128',
         '&sins;': 'ꞅ', '&Sins;': 'Ꞅ', '&tenl;': '\ueef5', '&tscap;': 'ᴛ',
         '&ttailstrok;': 'ꝷ', '&togon;': '\ue6ee', '&Togon;': '\ue2ee',
         '&tdotbl;': 'ṭ', '&Tdotbl;': 'Ṭ', '&tdot;': 'ṫ', '&Tdot;': 'Ṫ',
         '&tscapdot;': '\uef24', '&tscapdotbl;': '\uef2d',
         '&tacute;': '\ue6e2', '&Tacute;': '\ue2e2', '&trlig;': '\ueed8',
         '&ttlig;': '\ueed9', '&trottrotlig;': '\ueeda', '&tylig;': '\ueedb',
         '&tzlig;': '\ueedc', '&trot;': 'ꞇ', '&Trot;': 'Ꞇ',
         '&tcurl;': '\uf199', '&uenl;': '\ueef7', '&uscap;': 'ᴜ',
         '&ubar;': 'ʉ', '&uogon;': 'ų', '&Uogon;': 'Ų', '&ucurl;': '\ue731',
         '&Ucurl;': '\ue331', '&udotbl;': 'ụ', '&Udotbl;': 'Ụ',
         '&ubrevinvbl;': '\ue727', '&udot;': '\ue715', '&Udot;': '\ue315',
         '&uuml;': 'ü', '&Uuml;': 'Ü', '&uacute;': 'ú', '&Uacute;': 'Ú',
         '&udblac;': 'ű', '&Udblac;': 'Ű', '&udotacute;': '\uebff',
         '&Udotacute;': '\uebfe', '&ugrave;': 'ù', '&Ugrave;': 'Ù',
         '&uvertline;': '\ue724', '&Uvertline;': '\ue324', '&ucirc;': 'û',
         '&Ucirc;': 'Û', '&uumlcirc;': '\ue717', '&Uumlcirc;': '\ue317',
         '&ucar;': 'ǔ', '&Ucar;': 'Ǔ', '&uring;': 'ů', '&Uring;': 'Ů',
         '&uhook;': 'ủ', '&Uhook;': 'Ủ', '&ucurlbar;': '\uebbf',
         '&ubreve;': 'ŭ', '&Ubreve;': 'Ŭ', '&umacr;': 'ū', '&Umacr;': 'Ū',
         '&umacrbreve;': '\ue70b', '&Umacrbreve;': '\ue30b',
         '&umacracute;': '\ue709', '&Umacracute;': '\ue309', '&uumlmacr;': 'ǖ',
         '&Uumlmacr;': 'Ǖ', '&uelig;': '\ue8c9', '&UElig;': '\ue8c8',
         '&uulig;': '\ue8c7', '&UUlig;': '\ue8c6', '&uuligdblac;': '\uefd8',
         '&UUligdblac;': '\uefd9', '&uasup;': '\ue8eb', '&uesup;': '\ue72b',
         '&Uesup;': '\ue32b', '&uisup;': '\ue72c', '&uosup;': '\ue72d',
         '&Uosup;': '\ue32d', '&uvsup;': '\ue8ec', '&uwsup;': '\ue8ed',
         '&venl;': '\ueef8', '&vscap;': 'ᴠ', '&vbar;': '\ue74e',
         '&vslash;': '\ue8ba', '&vslashura;': '\ue8bb',
         '&vslashuradbl;': '\ue8bc', '&vdiagstrok;': 'ꝟ', '&Vdiagstrok;': 'Ꝟ',
         '&Vslstrok;': '℣', '&vdotbl;': 'ṿ', '&Vdotbl;': 'Ṿ',
         '&vdot;': '\ue74c', '&Vdot;': '\ue34c', '&vuml;': '\ue742',
         '&Vuml;': '\ue342', '&vacute;': '\ue73a', '&Vacute;': '\ue33a',
         '&vvertline;': '\ue74f', '&Vvertline;': '\ue34e',
         '&vdblac;': '\ue74b', '&Vdblac;': '\ue34b', '&vcirc;': '\ue73b',
         '&Vcirc;': '\ue33b', '&vring;': '\ue743', '&vmacr;': '\ue74d',
         '&Vmacr;': '\ue34d', '&Vovlhigh;': '\uf7b2', '&wynn;': 'ƿ',
         '&WYNN;': 'Ƿ', '&vins;': 'ꝩ', '&Vins;': 'Ꝩ', '&vinsdotbl;': '\ue7e6',
         '&Vinsdotbl;': '\ue3e6', '&vinsdot;': '\ue7e7', '&Vinsdot;': '\ue3e7',
         '&vinsacute;': '\uebbb', '&Vinsacute;': '\uebba', '&vwelsh;': 'ỽ',
         '&Vwelsh;': 'Ỽ', '&wenl;': '\ueef9', '&wscap;': 'ᴡ', '&wdotbl;': 'ẉ',
         '&Wdotbl;': 'Ẉ', '&wdot;': 'ẇ', '&Wdot;': 'Ẇ', '&wuml;': 'ẅ',
         '&Wuml;': 'Ẅ', '&wacute;': 'ẃ', '&Wacute;': 'Ẃ',
         '&wdblac;': '\ue750', '&Wdblac;': '\ue350', '&wgrave;': 'ẁ',
         '&Wgrave;': 'Ẁ', '&wcirc;': 'ŵ', '&Wcirc;': 'Ŵ', '&wring;': 'ẘ',
         '&wmacr;': '\ue757', '&Wmacr;': '\ue357', '&wasup;': '\ue8f0',
         '&wesup;': '\ue753', '&Wesup;': '\ue353', '&wisup;': '\ue8f1',
         '&wosup;': '\ue754', '&wusup;': '\ue8f2', '&wvsup;': '\ue8f3',
         '&xenl;': '\ueefa', '&xscap;': '\uef11', '&xmod;': 'ˣ', '&xdes;': 'ꭗ',
         '&xslashula;': '\ue8bd', '&xslashlra;': '\ue8be',
         '&xslashlradbl;': '\ue8ce', '&Xovlhigh;': '\uf7b3',
         '&yenl;': '\ueefb', '&yscap;': 'ʏ', '&ybar;': '\ue77b',
         '&ycurl;': '\ue785', '&Ycurl;': '\ue385', '&ydotbl;': 'ỵ',
         '&Ydotbl;': 'Ỵ', '&ydot;': 'ẏ', '&Ydot;': 'Ẏ', '&yuml;': 'ÿ',
         '&Yuml;': 'Ÿ', '&yacute;': 'ý', '&Yacute;': 'Ý', '&ydblac;': '\ue77c',
         '&Ydblac;': '\ue37c', '&ydotacute;': '\ue784',
         '&Ydotacute;': '\ue384', '&ygrave;': 'ỳ', '&Ygrave;': 'Ỳ',
         '&ycirc;': 'ŷ', '&Ycirc;': 'Ŷ', '&yring;': 'ẙ', '&yhook;': 'ỷ',
         '&Yhook;': 'Ỷ', '&ybreve;': '\ue776', '&Ybreve;': '\ue376',
         '&ymacr;': 'ȳ', '&Ymacr;': 'Ȳ', '&ymacrbreve;': '\ue775',
         '&Ymacrbreve;': '\ue375', '&ymacracute;': '\ue773',
         '&Ymacracute;': '\ue373', '&yylig;': 'ꝡ', '&YYlig;': 'Ꝡ',
         '&yyliguml;': '\uebe9', '&YYliguml;': '\uebe8',
         '&yyligdblac;': '\uebcb', '&YYligdblac;': '\uebca',
         '&yesup;': '\ue781', '&yrgmainstrok;': '\uf233', '&yloop;': 'ỿ',
         '&Yloop;': 'Ỿ', '&zenl;': '\ueefc', '&zscap;': 'ᴢ', '&zstrok;': 'ƶ',
         '&Zstrok;': 'Ƶ', '&zdotbl;': 'ẓ', '&Zdotbl;': 'Ẓ', '&zdot;': 'ż',
         '&Zdot;': 'Ż', '&zvisigot;': 'ꝣ', '&Zvisigot;': 'Ꝣ', '&ezh;': 'ʒ',
         '&EZH;': 'Ʒ', '&yogh;': 'ȝ', '&YOGH;': 'Ȝ', '&thorn;': 'þ',
         '&THORN;': 'Þ', '&thornenl;': '\ueef6', '&thornscap;': '\uef15',
         '&thornbar;': 'ꝥ', '&THORNbar;': 'Ꝥ', '&thornovlmed;': '\ue7a2',
         '&thornbarslash;': '\uf149', '&THORNbarslash;': '\ue337',
         '&thornbardes;': 'ꝧ', '&THORNbardes;': 'Ꝧ', '&thorndotbl;': '\ue79f',
         '&THORNdotbl;': '\ue39f', '&thornacute;': '\ue737',
         '&thornslonglig;': '\ue734', '&thornslongligbar;': '\ue735',
         '&thornrarmlig;': '\ue8c1', '&frac14;': '¼', '&frac12;': '½',
         '&frac34;': '¾', '&sup0;': '⁰', '&sup1;': '¹', '&sup2;': '²',
         '&sup3;': '³', '&sup4;': '⁴', '&sup5;': '⁵', '&sup6;': '⁶',
         '&sup7;': '⁷', '&sup8;': '⁸', '&sup9;': '⁹', '&sub0;': '₀',
         '&sub1;': '₁', '&sub2;': '₂', '&sub3;': '₃', '&sub4;': '₄',
         '&sub5;': '₅', '&sub6;': '₆', '&sub7;': '₇', '&sub8;': '₈',
         '&sub9;': '₉', '&romnumCDlig;': 'ↀ', '&romnumDDlig;': 'ↁ',
         '&romnumDDdbllig;': 'ↂ', '&romnumCrev;': 'Ↄ',
         '&romnumCrevovl;': '\uf23f', '&romnumCdblbar;': '\uf2fe',
         '&romnumcdblbar;': '\uf2ff', '&Imod;': 'ᴵ', '&Vmod;': 'ⱽ',
         '&Xmod;': '\uf1bf', '&asup;': 'ͣ', '&aeligsup;': 'ᷔ',
         '&anligsup;': '\uf036', '&anscapligsup;': '\uf03a', '&aoligsup;': 'ᷕ',
         '&arligsup;': '\uf038', '&arscapligsup;': '\uf130', '&avligsup;': 'ᷖ',
         '&bsup;': '\uf012', '&bscapsup;': '\uf013', '&csup;': 'ͨ',
         '&ccedilsup;': 'ᷗ', '&dsup;': 'ͩ', '&drotsup;': 'ᷘ', '&ethsup;': 'ᷙ',
         '&dscapsup;': '\uf016', '&esup;': 'ͤ', '&eogonsup;': '\uf135',
         '&emacrsup;': '\uf136', '&fsup;': '\uf017', '&gsup;': 'ᷚ',
         '&gscapsup;': 'ᷛ', '&hsup;': 'ͪ', '&isup;': 'ͥ',
         '&inodotsup;': '\uf02f', '&jsup;': '\uf030', '&jnodotsup;': '\uf031',
         '&ksup;': 'ᷜ', '&kscapsup;': '\uf01c', '&lsup;': 'ᷝ',
         '&lscapsup;': 'ᷞ', '&msup;': 'ͫ', '&mscapsup;': 'ᷟ', '&nsup;': 'ᷠ',
         '&nscapsup;': 'ᷡ', '&osup;': 'ͦ', '&omacrsup;': '\uf13f',
         '&oslashsup;': '\uf032', '&oogonsup;': '\uf13e',
         '&orrotsup;': '\uf03e', '&orumsup;': '\uf03f', '&psup;': '\uf025',
         '&qsup;': '\uf033', '&rsup;': 'ͬ', '&rrotsup;': 'ᷣ',
         '&rumsup;': '\uf040', '&rscapsup;': 'ᷢ', '&ssup;': 'ᷤ',
         '&slongsup;': 'ᷥ', '&tsup;': 'ͭ', '&trotsup;': '\uf03b',
         '&tscapsup;': '\uf02a', '&usup;': 'ͧ', '&vsup;': 'ͮ',
         '&wsup;': '\uf03c', '&xsup;': 'ͯ', '&ysup;': '\uf02b', '&zsup;': 'ᷦ',
         '&thornsup;': '\uf03d', '&combgrave;': '̀', '&combacute;': '́',
         '&combcirc;': '̂', '&combcircdbl;': '᷍', '&combtilde;': '̃',
         '&combmacr;': '̄', '&combbreve;': '̆', '&combdot;': '̇',
         '&combuml;': '̈', '&combhook;': '̉', '&combring;': '̊',
         '&combdblac;': '̋', '&combsgvertl;': '̍', '&combdbvertl;': '̎',
         '&combdotbl;': '̣', '&combced;': '̧', '&dblbarbl;': '̳',
         '&dblovl;': '̿', '&combogon;': '̨', '&combastbl;': '͙',
         '&combdblbrevebl;': '͜', '&combtripbrevebl;': '\uf1fc',
         '&combcurl;': '᷎', '&combcurlhigh;': '\uf1c5',
         '&combdothigh;': '\uf1ca', '&combcurlbar;': '\uf1cc', '&bar;': '̅',
         '&macrhigh;': '\uf00a', '&macrmed;': '\uf00b', '&ovlhigh;': '\uf00c',
         '&ovlmed;': '\uf00d', '&barbl;': '̲', '&baracr;': '̶',
         '&arbar;': '\uf1c0', '&combcomma;': '̕', '&combtildevert;': '̾',
         '&er;': '͛', '&erang;': '\uf1c7', '&ercurl;': '\uf1c8',
         '&ersub;': '᷏', '&ra;': 'ᷓ', '&rabar;': '\uf1c1', '&urrot;': '\uf153',
         '&urlemn;': '\uf1c2', '&ur;': '᷑', '&us;': '᷒', '&combisbelow;': '᷐',
         '&period;': '.', '&semi;': ';', '&amp;': '&', '&Theta;': 'Θ',
         '&theta;': 'θ', '&obiit;': 'ꝋ', '&OBIIT;': 'Ꝋ', '&et;': '⁊',
         '&etslash;': '\uf158', '&ET;': '\uf142', '&ETslash;': '\uf1a7',
         '&apomod;': 'ʼ', '&esse;': '≈', '&est;': '∻', '&condes;': 'ꝯ',
         '&CONdes;': 'Ꝯ', '&condot;': 'ꜿ', '&CONdot;': 'Ꜿ',
         '&usbase;': '\uf1a6', '&USbase;': '\uf1a5', '&usmod;': 'ꝰ',
         '&autem;': '\ue8a3', '&rum;': 'ꝝ', '&RUM;': 'Ꝝ', '&de;': '\uf159',
         '&is;': 'ꝭ', '&IS;': 'Ꝭ', '&sstrok;': 'ꝸ', '&etfin;': 'ꝫ',
         '&ETfin;': 'Ꝫ', '&sem;': '\uf1ac', '&fMedrun;': 'ᚠ', '&mMedrun;': 'ᛘ',
         '&lbbar;': '℔', '&circ;': '^', '&acute;': '´', '&grave;': '`',
         '&uml;': '¨', '&tld;': '~', '&macr;': '¯', '&breve;': '˘',
         '&dot;': '˙', '&ring;': '˚', '&cedil;': '¸', '&ogon;': '˛',
         '&tilde;': '˜', '&dblac;': '˝', '&verbarup;': 'ˈ', '&middot;': '·',
         '&hyphpoint;': '‧', '&sgldr;': '․', '&dblldr;': '‥', '&hellip;': '…',
         '&colon;': ':', '&comma;': ',', '&tridotright;': '჻',
         '&tridotupw;': '∴', '&tridotdw;': '∵', '&quaddot;': '∷',
         '&tridotleft;': '⁖', '&lozengedot;': '⁘', '&midring;': '\uf1da',
         '&verbar;': '|', '&brvbar;': '¦', '&Verbar;': '‖', '&sol;': '/',
         '&fracsol;': '⁄', '&dblsol;': '⫽', '&bsol;': '\\', '&luslst;': '⸌',
         '&ruslst;': '⸍', '&rlslst;': '⸜', '&llslst;': '⸝', '&lowbar;': '_',
         '&hyphen;': '-', '&dash;': '‐', '&nbhy;': '‑', '&dblhyph;': '⹀',
         '&dbloblhyph;': '⸗', '&numdash;': '‒', '&ndash;': '–', '&mdash;': '—',
         '&horbar;': '―', '&excl;': '!', '&iexcl;': '¡', '&quest;': '?',
         '&iquest;': '¿', '&ramus;': '\uf1db', '&lpar;': '(', '&rpar;': ')',
         '&lUbrack;': '⸦', '&rUbrack;': '⸧', '&ldblpar;': '⸨',
         '&rdblpar;': '⸩', '&lsqb;': '[', '&rsqb;': ']', '&lcub;': '{',
         '&rcub;': '}', '&lsqbqu;': '⁅', '&rsqbqu;': '⁆', '&lwhsqb;': '⟦',
         '&rwhsqb;': '⟧', '&verbarql;': '⸡', '&verbarqr;': '⸠',
         '&luhsqb;': '⸢', '&ruhsqb;': '⸣', '&llhsqb;': '⸤', '&rlhsqb;': '⸥',
         '&apos;': "'", '&prime;': '′', '&quot;': '"', '&Prime;': '″',
         '&lsquo;': '‘', '&rsquo;': '’', '&lsquolow;': '‚', '&rsquorev;': '‛',
         '&ldquo;': '“', '&rdquo;': '”', '&ldquolow;': '„', '&rdquorev;': '‟',
         '&lsaquo;': '‹', '&laquo;': '«', '&lt;': '<', '&langb;': '⟨',
         '&rsaquo;': '›', '&gt;': '>', '&raquo;': '»', '&rangb;': '⟩',
         '&hidot;': '\uf1f8', '&posit;': '\uf1e2', '&ductsimpl;': '\uf1e3',
         '&punctvers;': '\uf1ea', '&punctposit;': '\uf1e4',
         '&colmidcomposit;': '\uf1e5', '&bidotscomposit;': '\uf1f2',
         '&tridotscomposit;': '\uf1e6', '&punctelev;': '\uf161',
         '&punctelevdiag;': '\uf1f0', '&punctelevhiback;': '\uf1fa',
         '&punctelevhack;': '\uf1fb', '&punctflex;': '\uf1f5',
         '&punctexclam;': '\uf1e7', '&punctinter;': '\uf160',
         '&punctintertilde;': '\uf1e8', '&punctinterlemn;': '\uf1f1',
         '&punctpercont;': '⸮', '&wavylin;': '\uf1f9', '&medcom;': '\uf1e0',
         '&parag;': '\uf1e1', '&renvoi;': '\uf1ec', '&tridotsdownw;': '⸪',
         '&tridotsupw;': '⸫', '&quaddots;': '⸬', '&fivedots;': '⸭',
         '&virgsusp;': '\uf1f4', '&virgmin;': '\uf1f7', '&dipledot;': '⋗',
         '&sp;': ' ', '&nbsp;': '\xa0', '&nnbsp;': '\u202f',
         '&enqd;': '\u2000', '&emqd;': '\u2001', '&ensp;': '\u2002',
         '&emsp;': '\u2003', '&emsp13;': '\u2004', '&emsp14;': '\u2005',
         '&emsp16;': '\u2006', '&numsp;': '\u2007', '&puncsp;': '\u2008',
         '&thinsp;': '\u2009', '&hairsp;': '\u200a', '&zerosp;': '\u200b',
         '&del;': '\x7f', '&shy;': '\xad', '&num;': '#', '&sect;': '§',
         '&ast;': '*', '&triast;': '⁂', '&commat;': '@', '&copy;': '©',
         '&reg;': '®', '&not;': '¬', '&logand;': '∧', '&para;': '¶',
         '&revpara;': '⁋', '&cross;': '✝', '&dagger;': '†', '&Dagger;': '‡',
         '&tridagger;': '\uf1d2', '&refmark;': '※', '&dotcross;': '⁜',
         '&hedera;': '❦', '&hederarot;': '❧', '&dollar;': '$', '&cent;': '¢',
         '&pound;': '£', '&curren;': '¤', '&yen;': '¥', '&pennygerm;': '₰',
         '&scruple;': '℈', '&romaslibr;': '\uf2e0', '&romXbar;': '\uf2e1',
         '&romscapxbar;': '\uf2e2', '&romscapybar;': '\uf2e3',
         '&romscapdslash;': '\uf2e4', '&drotbar;': '\uf159', '&ecu;': '\uf2e7',
         '&florloop;': '\uf2e8', '&grosch;': '\uf2e9', '&helbing;': '\uf2fb',
         '&krone;': '\uf2fa', '&libradut;': '\uf2ea', '&librafren;': '\uf2eb',
         '&libraital;': '\uf2ec', '&libraflem;': '\uf2ed',
         '&liranuov;': '\uf2ee', '&lirasterl;': '\uf2ef',
         '&markold;': '\uf2f0', '&markflour;': '\uf2f1', '&msign;': '\uf2f2',
         '&msignflour;': '\uf2f3', '&penningar;': '\uf2f5',
         '&reichtalold;': '\uf2f6', '&schillgerm;': '\uf2f7',
         '&schillgermscript;': '\uf2f8', '&scudi;': '\uf2f9', '&ounce;': '℥',
         '&sestert;': '\uf2fa', '&romas;': '\uf2d8', '&romunc;': '\uf2d9',
         '&romsemunc;': '\uf2da', '&romsext;': '\uf2db',
         '&romdimsext;': '\uf2dc', '&romsiliq;': '\uf2dd',
         '&romquin;': '\uf2de', '&romdupond;': '\uf2df', '&plus;': '+',
         '&minus;': '−', '&plusmn;': '±', '&times;': '×', '&divide;': '÷',
         '&equals;': '=', '&infin;': '∞', '&notequals;': '≠', '&percnt;': '%',
         '&permil;': '‰', '&deg;': '°', '&smallzero;': '\uf1bd',
         '&micro;': 'µ', '&dram;': '\uf2e6', '&obol;': '\uf2f4',
         '&sextans;': '\uf2fb', '&ouncescript;': '\uf2fd', '&arrsgllw;': '←',
         '&arrsglupw;': '↑', '&arrsglrw;': '→', '&arrsgldw;': '↓',
         '&squareblsm;': '▪', '&squarewhsm;': '▫', '&bull;': '•',
         '&circledot;': '◌', '&tribull;': '‣', '&trirightwh;': '▹',
         '&trileftwh;': '◃', '&metrshort;': '⏑', '&metrshortlong;': '⏒',
         '&metrlongshort;': '⏓', '&metrdblshortlong;': '⏔',
         '&metranc;': '\uf70a', '&metrancacute;': '\uf70b',
         '&metrancdblac;': '\uf719', '&metrancgrave;': '\uf70c',
         '&metrancdblgrave;': '\uf71a', '&metrbreve;': '\uf701',
         '&metrbreveacute;': '\uf706', '&metrbrevedblac;': '\uf717',
         '&metrbrevegrave;': '\uf707', '&metrbrevedblgrave;': '\uf718',
         '&metrmacr;': '\uf700', '&metrmacracute;': '\uf704',
         '&metrmacrdblac;': '\uf715', '&metrmacrgrave;': '\uf705',
         '&metrmacrdblgrave;': '\uf716', '&metrmacrbreve;': '\uf702',
         '&metrbrevemacr;': '\uf703', '&metrmacrbreveacute;': '\uf708',
         '&metrmacrbrevegrave;': '\uf709', '&metrdblbrevemacr;': '\uf72e',
         '&metrdblbrevemacracute;': '\uf71b',
         '&metrdblbrevemacrdblac;': '\uf71c', '&metrpause;': '\uf714'}
MUFI4_KEYS = "&aenl;&ascap;&ordf;&aogon;&Aogon;&acurl;&Acurl;&adotbl;" \
             "&Adotbl;&adot;&Adot;&auml;&Auml;&adiaguml;&adotbluml;&aacute;" \
             "&Aacute;&aenlacute;&aogonacute;&Aogonacute;&adblac;&Adblac;" \
             "&adotacute;&Adotacute;&agrave;&Agrave;&acirc;&Acirc;&aumlcirc;" \
             "&aringcirc;&atilde;&Atilde;&aring;&Aring;&ahook;&Ahook;" \
             "&abreve;&Abreve;&amacr;&Amacr;&amacrbreve;&Amacrbreve;" \
             "&abreveacute;&Abreveacute;&amacracute;&Amacracute;&aalig;" \
             "&aacloselig;&AAlig;&aaligenl;&aaligdotbl;&AAligdotbl;" \
             "&aaligdot;&AAligdot;&aaliguml;&AAliguml;&aaligacute;" \
             "&AAligacute;&aaligdblac;&AAligdblac;&aelig;&AElig;&aeligenl;" \
             "&aeligscap;&aeligred;&aeligcurl;&AEligcurl;&aeligogon;" \
             "&AEligogon;&aeligdotbl;&AEligdotbl;&aeligdot;&AEligdot;" \
             "&aeliguml;&AEliguml;&aeligacute;&AEligacute;&aeligogonacute;" \
             "&aeligdblac;&AEligdblac;&aeligring;&aeligbreve;&AEligbreve;" \
             "&aeligmacr;&AEligmacr;&aeligmacrbreve;&AEligmacrbreve;" \
             "&aeligmacracute;&AEligmacracute;&aeligdotacute;&AEligdotacute;" \
             "&aflig;&afinslig;&aglig;&allig;&anlig;&anscaplig;&aolig;" \
             "&AOlig;&aoligenl;&aenlosmalllig;&aoligred;&AOligred;" \
             "&aoligdotbl;&AOligdotbl;&aoligacute;&AOligacute;&aoligdblac;" \
             "&AOligdblac;&aplig;&arlig;&arscaplig;&aulig;&AUlig;" \
             "&auligdotbl;&AUligdotbl;&auligacute;&AUligacute;&avlig;&AVlig;" \
             "&avligslash;&AVligslash;&avligslashacute;&AVligslashacute;" \
             "&avligogon;&AVligogon;&avligdotbl;&AVligdotbl;&avligacute;" \
             "&AVligacute;&avligdblac;&AVligdblac;&aylig;&AYlig;&ayligdotbl;" \
             "&AYligdotbl;&ayligdot;&AYligdot;&athornlig;&aesup;&Aesup;" \
             "&iesup;&aosup;&ausup;&avsup;&aunc;&aopen;&ains;&Ains;" \
             "&aneckless;&anecklesselig;&AnecklessElig;&anecklessvlig;" \
             "&aclose;&Asqu;&benl;&bscap;&bscapdot;&bscapdotbl;&bdotbl;" \
             "&Bdotbl;&bdot;&Bdot;&bacute;&Bacute;&bstrok;&bovlmed;&bblig;" \
             "&bglig;&cenl;&cscap;&ccedil;&Ccedil;&cogon;&Cogon;&cdotbl;" \
             "&Cdotbl;&cdot;&Cdot;&cacute;&Cacute;&Covlhigh;&chlig;&cklig;" \
             "&ctlig;&Csqu;&ccurl;&CONbase;&conbase;&denl;&dscap;&dstrok;" \
             "&Dstrok;&dovlmed;&dtailstrok;&dtail;&dscapdot;&ddotbl;&Ddotbl;" \
             "&dscapdotbl;&ddot;&Ddot;&dacute;&Dacute;&eth;&ETH;&ethenl;" \
             "&ethscap;&ethdotbl;&ETHdotbl;&Dovlhigh;&drotdrotlig;&Drot;" \
             "&drot;&drotdot;&drotacute;&drotenl;&dscript;&dcurl;&eenl;" \
             "&escap;&eogon;&Eogon;&ecurl;&Ecurl;&eogoncurl;&Eogoncurl;" \
             "&edotbl;&Edotbl;&eogondot;&Eogondot;&eogondotbl;&Eogondotbl;" \
             "&eogonenl;&edot;&Edot;&euml;&Euml;&eumlmacr;&eacute;&Eacute;" \
             "&eogonacute;&Eogonacute;&edotblacute;&edblac;&Edblac;" \
             "&edotacute;&Edotacute;&eogondotacute;&Eogondotacute;" \
             "&eogondblac;&Eogondblac;&egrave;&Egrave;&ecirc;&Ecirc;" \
             "&eogoncirc;&ering;&ebreve;&Ebreve;&emacr;&Emacr;&eogonmacr;" \
             "&Eogonmacr;&emacrbreve;&Emacrbreve;&emacracute;&Emacracute;" \
             "&eylig;&eacombcirc;&eucombcirc;&easup;&Easup;&eesup;&eisup;" \
             "&eosup;&evsup;&schwa;&Eunc;&Euncclose;&eunc;&eext;&etall;" \
             "&fenl;&fscap;&fdotbl;&Fdotbl;&fdot;&Fdot;&fscapdot;&facute;" \
             "&Facute;&faumllig;&fflig;&filig;&fjlig;&foumllig;" \
             "&fllig;&frlig;&ftlig;&fuumllig;&fylig;&ffilig;&ffllig;&fftlig;" \
             "&ffylig;&ftylig;&fturn;&Fturn;&Frev;&fins;&Fins;&finsenl;" \
             "&finsdot;&Finsdot;&finsdothook;&finssemiclose;" \
             "&finssemiclosedot;&finsclose;&finsclosedot;&finsdotbl;" \
             "&Finsdotbl;&finsacute;&Finsacute;&fcurl;&genl;&gscap;&gstrok;" \
             "&Gstrok;&gdotbl;&Gdotbl;&gscapdotbl;&gdot;&Gdot;&gscapdot;" \
             "&Gacute;&gacute;&gglig;&gdlig;&gdrotlig;&gethlig;&golig;" \
             "&gplig;&grlig;&gins;&Gins;&ginsturn;&Ginsturn;&Gsqu;&gdivloop;" \
             "&glglowloop;&gsmlowloop;&gopen;&gcurl;&henl;&hscap;&hhook;" \
             "&hstrok;&hovlmed;&hdotbl;&Hdotbl;&Hdot;&hdot;&hscapdot;" \
             "&hacute;&Hacute;&hwair;&HWAIR;&hslonglig;&hslongligbar;" \
             "&hrarmlig;&Hrarmlig;&hhalf;&Hhalf;&Hunc;&hrdes;&ienl;&iscap;" \
             "&inodot;&inodotenl;&Idot;&istrok;&idblstrok;&iogon;" \
             "&inodotogon;&Iogon;&icurl;&Icurl;&idotbl;&Idotbl;&ibrevinvbl;" \
             "&iuml;&Iuml;&iacute;&Iacute;&idblac;&Idblac;&idotacute;" \
             "&Idotacute;&igrave;&Igrave;&icirc;&Icirc;&ihook;&Ihook;" \
             "&ibreve;&Ibreve;&imacr;&Imacr;&iovlmed;&Iovlhigh;&imacrbreve;" \
             "&Imacrbreve;&imacracute;&Imacracute;&ijlig;&IJlig;&iasup;" \
             "&iosup;&iusup;&ivsup;&ilong;&Ilong;&jenl;&jscap;&jnodot;" \
             "&jnodotenl;&Jdot;&jnodotstrok;&jbar;&jdblstrok;&Jbar;&jcurl;" \
             "&Jcurl;&juml;&Juml;&jdotbl;&Jdotbl;&jacute;&Jacute;&jdblac;" \
             "&Jdblac;&jmacrmed;&jovlmed;&Jmacrhigh;&Jovlhigh;&jesup;&kenl;" \
             "&kscap;&khook;&kbar;&Kbar;&kovlmed;&kstrleg;&Kstrleg;" \
             "&kstrascleg;&Kstrascleg;&kdot;&Kdot;&kscapdot;&kdotbl;&Kdotbl;" \
             "&kacute;&Kacute;&kslonglig;&kslongligbar;&krarmlig;&kunc;" \
             "&ksemiclose;&kclose;&kcurl;&lenl;&lscap;&lbar;&lstrok;&Lstrok;" \
             "&lhighstrok;&Lhighstrok;&lovlmed;&ltailstrok;&ldotbl;&Ldotbl;" \
             "&lscapdotbl;&ldot;&Ldot;&lscapdot;&lacute;&Lacute;&lringbl;" \
             "&lmacrhigh;&lovlhigh;&Lovlhigh;&lbrk;&Lbrk;&llwelsh;&LLwelsh;" \
             "&lllig;&ldes;&lturn;&Lturn;&menl;&mscap;&mtailstrok;&mdotbl;" \
             "&Mdotbl;&mscapdotbl;&mdot;&Mdot;&mscapdot;&macute;&Macute;" \
             "&mringbl;&mmacrmed;&Mmacrhigh;&movlmed;&Movlhigh;&mesup;&Minv;" \
             "&mturn;&Mturn;&munc;&mmedunc;&Munc;&mrdes;&muncdes;" \
             "&mmeduncdes;&Muncdes;&muncacute;&mmeduncacute;&Muncacute;" \
             "&M5leg;&nenl;&nscap;&nscapldes;&nlrleg;&nlfhook;&nbar;" \
             "&ntailstrok;&ndot;&Ndot;&nscapdot;&nacute;&Nacute;&ndotbl;" \
             "&Ndotbl;&nscapdotbl;&ncirc;&ntilde;&Ntilde;&nringbl;&nmacrmed;" \
             "&Nmacrhigh;&eng;&ENG;&nscapslonglig;&nrdes;&Nrdes;&nscaprdes;" \
             "&nflour;&oenl;&oscap;&ordm;&oogon;&Oogon;&ocurl;&Ocurl;" \
             "&oogoncurl;&Oogoncurl;&ocurlacute;&Ocurlacute;&oslash;&Oslash;" \
             "&oslashcurl;&Oslashcurl;&oslashogon;&Oslashogon;&odotbl;" \
             "&Odotbl;&oslashdotbl;&Oslashdotbl;&odot;&Odot;&oogondot;" \
             "&Oogondot;&oogonmacr;&Oogonmacr;&oslashdot;&Oslashdot;" \
             "&oogondotbl;&Oogondotbl;&ouml;&Ouml;&odiaguml;&oumlacute;" \
             "&oacute;&Oacute;&oslashacute;&Oslashacute;&oslashdblac;" \
             "&Oslashdblac;&oogonacute;&Oogonacute;&oslashogonacute;" \
             "&Oslashogonacute;&odblac;&Odblac;&odotacute;&Odotacute;" \
             "&oogondotacute;&Oogondotacute;&oslashdotacute;&Oslashdotacute;" \
             "&oogondblac;&Oogondblac;&ograve;&Ograve;&ocirc;&Ocirc;" \
             "&oumlcirc;&Oumlcirc;&oogoncirc;&ocar;&Ocar;&otilde;&Otilde;" \
             "&oring;&ohook;&Ohook;&obreve;&Obreve;&oslashbreve;" \
             "&Oslashbreve;&omacr;&Omacr;&oslashmacr;&Oslashmacr;" \
             "&omacrbreve;&Omacrbreve;&oslashmacrbreve;&Oslashmacrbreve;" \
             "&omacracute;&Omacracute;&oslashmacracute;&Oslashmacracute;" \
             "&oumlmacr;&Oumlmacr;&oclig;&oelig;&OElig;&oeligscap;&oeligenl;" \
             "&oeligogon;&OEligogon;&Oloop;&oloop;&oeligacute;&OEligacute;" \
             "&oeligdblac;&OEligdblac;&oeligmacr;&OEligmacr;&oeligmacrbreve;" \
             "&OEligmacrbreve;&oolig;&OOlig;&ooliguml;&OOliguml;&ooligacute;" \
             "&OOligacute;&ooligdblac;&OOligdblac;&ooligdotbl;&OOligdotbl;" \
             "&orrotlig;&oasup;&oesup;&Oesup;&oisup;&oosup;&ousup;&Ousup;" \
             "&ovsup;&oopen;&oopenmacr;&penl;&pscap;&pbardes;&Pbardes;" \
             "&pflour;&Pflour;&psquirrel;&Psquirrel;&pdotbl;&Pdotbl;&pdot;" \
             "&Pdot;&pscapdot;&pacute;&Pacute;&pdblac;&Pdblac;&pmacr;&pplig;" \
             "&PPlig;&ppflourlig;&ppliguml;&PPliguml;&Prev;&qenl;&qscap;" \
             "&qslstrok;&Qslstrok;&qbardes;&Qbardes;&qbardestilde;&q2app;" \
             "&q3app;&qcentrslstrok;&qdotbl;&Qdotbl;&qdot;&Qdot;&qmacr;" \
             "&qvinslig;&Qstem;&renl;&rscap;&YR;&rdes;&rdesstrok;" \
             "&rtailstrok;&rscaptailstrok;&Rtailstrok;&Rslstrok;&rdotbl;" \
             "&Rdotbl;&rdot;&Rdot;&rscapdot;&racute;&Racute;&rringbl;" \
             "&rscapdotbl;&resup;&rrot;&Rrot;&rrotdotbl;&rrotacute;&rins;" \
             "&Rins;&rflour;&senl;&sscap;&sdot;&Sdot;&sscapdot;&sacute;" \
             "&Sacute;&sdotbl;&Sdotbl;&sscapdotbl;&szlig;&SZlig;" \
             "&slongaumllig;&slongchlig;&slonghlig;&slongilig;&slongjlig;" \
             "&slongklig;&slongllig;&slonglbarlig;&slongoumllig;&slongplig;" \
             "&slongslig;&slongslonglig;&slongslongilig;&slongslongklig;&" \
             "slongslongllig;&slongslongtlig;&stlig;&slongtlig;&slongtilig;" \
             "&slongtrlig;&slonguumllig;&slongvinslig;&slongdestlig;&slong;" \
             "&slongenl;&slongbarslash;&slongbar;&slongovlmed;&slongslstrok;" \
             "&slongflour;&slongacute;&slongdes;&slongdotbl;&Sclose;&sclose;" \
             "&sins;&Sins;&tenl;&tscap;&ttailstrok;&togon;&Togon;&tdotbl;" \
             "&Tdotbl;&tdot;&Tdot;&tscapdot;&tscapdotbl;&tacute;&Tacute;" \
             "&trlig;&ttlig;&trottrotlig;&tylig;&tzlig;&trot;&Trot;&tcurl;" \
             "&uenl;&uscap;&ubar;&uogon;&Uogon;&ucurl;&Ucurl;&udotbl;" \
             "&Udotbl;&ubrevinvbl;&udot;&Udot;&uuml;&Uuml;&uacute;&Uacute;" \
             "&udblac;&Udblac;&udotacute;&Udotacute;&ugrave;&Ugrave;" \
             "&uvertline;&Uvertline;&ucirc;&Ucirc;&uumlcirc;&Uumlcirc;&ucar;" \
             "&Ucar;&uring;&Uring;&uhook;&Uhook;&ucurlbar;&ubreve;&Ubreve;" \
             "&umacr;&Umacr;&umacrbreve;&Umacrbreve;&umacracute;&Umacracute;" \
             "&uumlmacr;&Uumlmacr;&uelig;&UElig;&uulig;&UUlig;&uuligdblac;" \
             "&UUligdblac;&uasup;&uesup;&Uesup;&uisup;&uosup;&Uosup;&uvsup;" \
             "&uwsup;&venl;&vscap;&vbar;&vslash;&vslashura;&vslashuradbl;" \
             "&vdiagstrok;&Vdiagstrok;&Vslstrok;&vdotbl;&Vdotbl;&vdot;&Vdot;" \
             "&vuml;&Vuml;&vacute;&Vacute;&vvertline;&Vvertline;&vdblac;" \
             "&Vdblac;&vcirc;&Vcirc;&vring;&vmacr;&Vmacr;&Vovlhigh;&wynn;" \
             "&WYNN;&vins;&Vins;&vinsdotbl;&Vinsdotbl;&vinsdot;&Vinsdot;" \
             "&vinsacute;&Vinsacute;&vwelsh;&Vwelsh;&wenl;&wscap;&wdotbl;" \
             "&Wdotbl;&wdot;&Wdot;&wuml;&Wuml;&wacute;&Wacute;&wdblac;" \
             "&Wdblac;&wgrave;&Wgrave;&wcirc;&Wcirc;&wring;&wmacr;&Wmacr;" \
             "&wasup;&wesup;&Wesup;&wisup;&wosup;&wusup;&wvsup;&xenl;&xscap;" \
             "&xmod;&xdes;&xslashula;&xslashlra;&xslashlradbl;&Xovlhigh;" \
             "&yenl;&yscap;&ybar;&ycurl;&Ycurl;&ydotbl;&Ydotbl;&ydot;&Ydot" \
             ";&yuml;&Yuml;&yacute;&Yacute;&ydblac;&Ydblac;&ydotacute;" \
             "&Ydotacute;&ygrave;&Ygrave;&ycirc;&Ycirc;&yring;&yhook;&Yhook;" \
             "&ybreve;&Ybreve;&ymacr;&Ymacr;&ymacrbreve;&Ymacrbreve;" \
             "&ymacracute;&Ymacracute;&yylig;&YYlig;&yyliguml;&YYliguml;" \
             "&yyligdblac;&YYligdblac;&yesup;&yrgmainstrok;&yloop;&Yloop;" \
             "&zenl;&zscap;&zstrok;&Zstrok;&zdotbl;&Zdotbl;&zdot;&Zdot;" \
             "&zvisigot;&Zvisigot;&ezh;&EZH;&yogh;&YOGH;&thorn;&THORN;" \
             "&thornenl;&thornscap;&thornbar;&THORNbar;&thornovlmed;" \
             "&thornbarslash;&THORNbarslash;&thornbardes;&THORNbardes;" \
             "&thorndotbl;&THORNdotbl;&thornacute;&thornslonglig;" \
             "&thornslongligbar;&thornrarmlig;&frac14;&frac12;&frac34;&sup0;" \
             "&sup1;&sup2;&sup3;&sup4;&sup5;&sup6;&sup7;&sup8;&sup9;&sub0;" \
             "&sub1;&sub2;&sub3;&sub4;&sub5;&sub6;&sub7;&sub8;&sub9;" \
             "&romnumCDlig;&romnumDDlig;&romnumDDdbllig;&romnumCrev;" \
             "&romnumCrevovl;&romnumCdblbar;&romnumcdblbar;&Imod;&Vmod;" \
             "&Xmod;&asup;&aeligsup;&anligsup;&anscapligsup;&aoligsup;" \
             "&arligsup;&arscapligsup;&avligsup;&bsup;&bscapsup;&csup;" \
             "&ccedilsup;&dsup;&drotsup;&ethsup;&dscapsup;&esup;&eogonsup;" \
             "&emacrsup;&fsup;&gsup;&gscapsup;&hsup;&isup;&inodotsup;&jsup;" \
             "&jnodotsup;&ksup;&kscapsup;&lsup;&lscapsup;&msup;&mscapsup;" \
             "&nsup;&nscapsup;&osup;&omacrsup;&oslashsup;&oogonsup;" \
             "&orrotsup;&orumsup;&psup;&qsup;&rsup;&rrotsup;&rumsup;" \
             "&rscapsup;&ssup;&slongsup;&tsup;&trotsup;&tscapsup;&usup;" \
             "&vsup;&wsup;&xsup;&ysup;&zsup;&thornsup;&combgrave;&combacute;" \
             "&combcirc;&combcircdbl;&combtilde;&combmacr;&combbreve;" \
             "&combdot;&combuml;&combhook;&combring;&combdblac;&combsgvertl;" \
             "&combdbvertl;&combdotbl;&combced;&dblbarbl;&dblovl;&combogon;" \
             "&combastbl;&combdblbrevebl;&combtripbrevebl;&combcurl;" \
             "&combcurlhigh;&combdothigh;&combcurlbar;&bar;&macrhigh;" \
             "&macrmed;&ovlhigh;&ovlmed;&barbl;&baracr;&arbar;&combcomma;" \
             "&combtildevert;&er;&erang;&ercurl;&ersub;&ra;&rabar;&urrot;" \
             "&urlemn;&ur;&us;&combisbelow;&period;&semi;&amp;&Theta;&theta;" \
             "&obiit;&OBIIT;&et;&etslash;&ET;&ETslash;&apomod;&esse;&est;" \
             "&condes;&CONdes;&condot;&CONdot;&usbase;&USbase;&usmod;&autem;" \
             "&rum;&RUM;&de;&is;&IS;&sstrok;&etfin;&ETfin;&sem;&fMedrun;" \
             "&mMedrun;&lbbar;&circ;&acute;&grave;&uml;&tld;&macr;&breve;" \
             "&dot;&ring;&cedil;&ogon;&tilde;&dblac;&verbarup;&middot;" \
             "&hyphpoint;&sgldr;&dblldr;&hellip;&colon;&comma;&tridotright;" \
             "&tridotupw;&tridotdw;&quaddot;&tridotleft;&lozengedot;" \
             "&midring;&verbar;&brvbar;&Verbar;&sol;&fracsol;&dblsol;&bsol;" \
             "&luslst;&ruslst;&rlslst;&llslst;&lowbar;&hyphen;&dash;&nbhy;" \
             "&dblhyph;&dbloblhyph;&numdash;&ndash;&mdash;&horbar;&excl;" \
             "&iexcl;&quest;&iquest;&ramus;&lpar;&rpar;&lUbrack;&rUbrack;" \
             "&ldblpar;&rdblpar;&lsqb;&rsqb;&lcub;&rcub;&lsqbqu;&rsqbqu;" \
             "&lwhsqb;&rwhsqb;&verbarql;&verbarqr;&luhsqb;&ruhsqb;&llhsqb;" \
             "&rlhsqb;&apos;&prime;&quot;&Prime;&lsquo;&rsquo;&lsquolow;" \
             "&rsquorev;&ldquo;&rdquo;&ldquolow;&rdquorev;&lsaquo;&laquo;" \
             "&lt;&langb;&rsaquo;&gt;&raquo;&rangb;&hidot;&posit;&ductsimpl;" \
             "&punctvers;&punctposit;&colmidcomposit;&bidotscomposit;" \
             "&tridotscomposit;&punctelev;&punctelevdiag;&punctelevhiback;" \
             "&punctelevhack;&punctflex;&punctexclam;&punctinter;" \
             "&punctintertilde;&punctinterlemn;&punctpercont;&wavylin;" \
             "&medcom;&parag;&renvoi;&tridotsdownw;&tridotsupw;&quaddots;" \
             "&fivedots;&virgsusp;&virgmin;&dipledot;&sp;&nbsp;&nnbsp;&enqd;" \
             "&emqd;&ensp;&emsp;&emsp13;&emsp14;&emsp16;&numsp;&puncsp;" \
             "&thinsp;&hairsp;&zerosp;&del;&shy;&num;&sect;&ast;&triast;" \
             "&commat;&copy;&reg;&not;&logand;&para;&revpara;&cross;&dagger;" \
             "&Dagger;&tridagger;&refmark;&dotcross;&hedera;&hederarot;" \
             "&dollar;&cent;&pound;&curren;&yen;&pennygerm;&scruple;" \
             "&romaslibr;&romXbar;&romscapxbar;&romscapybar;&romscapdslash;" \
             "&drotbar;&ecu;&florloop;&grosch;&helbing;&krone;&libradut;" \
             "&librafren;&libraital;&libraflem;&liranuov;&lirasterl;" \
             "&markold;&markflour;&msign;&msignflour;&penningar;" \
             "&reichtalold;&schillgerm;&schillgermscript;&scudi;&ounce;" \
             "&sestert;&romas;&romunc;&romsemunc;&romsext;&romdimsext;" \
             "&romsiliq;&romquin;&romdupond;&plus;&minus;&plusmn;&times;" \
             "&divide;&equals;&infin;&notequals;&percnt;&permil;&deg;" \
             "&smallzero;&micro;&dram;&obol;&sextans;&ouncescript;&arrsgllw;" \
             "&arrsglupw;&arrsglrw;&arrsgldw;&squareblsm;&squarewhsm;&bull;" \
             "&circledot;&tribull;&trirightwh;&trileftwh;&metrshort;" \
             "&metrshortlong;&metrlongshort;&metrdblshortlong;&metranc;" \
             "&metrancacute;&metrancdblac;&metrancgrave;&metrancdblgrave;" \
             "&metrbreve;&metrbreveacute;&metrbrevedblac;&metrbrevegrave;" \
             "&metrbrevedblgrave;&metrmacr;&metrmacracute;&metrmacrdblac;" \
             "&metrmacrgrave;&metrmacrdblgrave;&metrmacrbreve;" \
             "&metrbrevemacr;&metrmacrbreveacute;&metrmacrbrevegrave;" \
             "&metrdblbrevemacr;&metrdblbrevemacracute;" \
             "&metrdblbrevemacrdblac;&metrpause;"
MUFI4_VALS = "ᴀªąĄạẠȧȦäÄáÁàÀâÂãÃåÅảẢăĂāĀắẮꜳꜲ" \
             "æÆᴁǽǼǣǢ" \
             "ꜵꜴꜷꜶꜹꜸꜻꜺꜽꜼ" \
             "ʙḅḄḃḂƀᴄçÇċĊćĆ" \
             "ↃↄᴅđĐꝱɖḍḌḋḊðÐᴆꝹꝺẟᴇęĘẹẸ" \
             "ėĖëËéÉèÈêÊĕĔēĒḗḖəꜰḟ" \
             "ḞﬀﬁﬂﬃﬄⅎℲꟻꝼꝻɢǥǤġĠ" \
             "ǴǵᵹꝽꝿꝾɡʜɦħḥḤḣḢƕǶⱶⱵɪıİɨįĮ" \
             "ịỊïÏíÍìÌîÎỉỈĭĬīĪĳĲꟾᴊȷɟɉɈ" \
             "ᴋƙꝁꝀꝃꝂꝅꝄḳḲḱḰʟƚłŁꝉꝈꝲḷḶĺĹꝇꝆỻỺꞁ" \
             "ꞀᴍꝳṃṂṁṀḿḾꟽɯƜꟿɴƞɲꝴṅṄńŃṇṆ" \
             "ñÑŋŊᴏºǫǪøØọỌȯȮǭǬöÖóÓ" \
             "ǿǾőŐòÒôÔǒǑõÕỏỎŏŎōŌṓṒȫȪœ" \
             "ŒɶꝌꝍꝏꝎɔᴘꝑꝐꝓꝒꝕꝔṗṖṕ" \
             "ṔꟼꝙꝘꝗꝖʀƦɼꝵꝶ℞℟ṛṚṙṘŕŔꝛꝚ" \
             "ꞃꞂꜱṡṠśŚṣṢßẞﬆﬅſẜẝ" \
             "ꞅꞄᴛꝷṭṬṫṪꞇꞆᴜʉųŲụỤüÜúÚűŰùÙûÛ" \
             "ǔǓůŮủỦŭŬūŪǖǕᴠꝟꝞ℣ṿṾ" \
             "ƿǷꝩꝨỽỼᴡẉẈẇẆẅẄẃẂẁẀŵŴẘˣꭗʏỵỴẏẎ" \
             "ÿŸýÝỳỲŷŶẙỷỶȳȲꝡꝠỿỾᴢƶƵẓẒżŻꝣꝢʒƷȝȜþÞꝥꝤꝧꝦ" \
             "¼½¾⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉ↀↁↂↃᴵⱽͣᷔᷕᷖͨᷗͩᷘᷙͤᷚᷛͪͥ" \
             "ᷜᷝᷞͫᷟᷠᷡͦͬᷣᷢᷤᷥͭͧͮͯᷦ̧̨̣̳͙̀́̂̃̄̆̇̈̉̊̋̍̎̿͜᷍᷎̅" \
             "̶̲̾͛̕᷏ᷓ᷐᷑᷒.;&ΘθꝋꝊ⁊ʼ≈∻ꝯꝮꜿꜾꝰꝝꝜꝭꝬꝸꝫꝪᚠᛘ℔^´`¨~¯˘˙" \
             "˚¸˛˜˝ˈ·‧․‥…:,჻∴∵∷⁖⁘|¦‖/⁄⫽\⸌⸍⸜⸝_-‐‑⹀⸗‒–—―!¡?¿()⸦⸧⸨⸩[]{}⁅⁆⟦⟧⸡⸠" \
             "⸢⸣⸤⸥'′\"″‘’‚‛“”„‟‹«<⟨›>»⟩⸮⸪" \
             "⸫⸬⸭⋗              ​­#§*⁂@©®¬∧¶⁋✝†‡※⁜❦❧$¢£¤¥₰℈" \
             "℥+−±×÷=∞≠%‰°µ" \
             "←↑→↓▪▫•◌‣▹◃⏑⏒⏓⏔"
PUNCT_SYMBOL_VALS = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~¡¢£¤¥¦§¨©«¬®¯°±´¶·¸" \
                    "»¿×÷˂˃˄˅˒˓˔˕˖˗˘˙˚˛˜˝˞˟˥˦˧˨˩˪˫˭˯˰˱˲˳˴˵˶˷˸˹˺˻˼˽˾˿͵;΄΅·϶҂՚" \
                    "՛՜՝՞՟։֊֍֎֏" \
                    "־׀׃׆׳״؆؇؈؉؊؋،؍؎؏؛؞؟٪٫٬٭۔۞" \
                    "۩۽۾܀܁܂܃܄܅܆܇܈܉܊܋܌܍߶߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾࡞।॥॰৲৳৺৻૰૱୰௳௴௵௶௷௸" \
                    "௹௺౿൏൹෴฿๏๚๛༁༂༃༄༅༆༇༈༉༊་༌།༎༏༐༑༒༓༔༕༖༗༚༛༜༝༞༟༴༶༸༺༻༼༽྅" \
                    "྾྿࿀࿁࿂࿃࿄࿅࿇࿈࿉࿊࿋࿌࿎࿏࿐࿑࿒࿓࿔࿕࿖࿗࿘࿙࿚၊။၌၍၎၏႞႟჻፠፡።፣፤፥፦፧፨᎐᎑᎒᎓᎔" \
                    "᎕᎖᎗᎘᎙᐀᙭᙮᚛᚜᛫᛬᛭᜵᜶។៕៖៘៙៚៛᠀᠁᠂᠃᠄᠅᠆᠇᠈᠉᠊᥀᥄᥅᧞᧟᧠᧡᧢᧣᧤᧥᧦᧧᧨᧩᧪" \
                    "᧫᧬᧭᧮᧯᧰᧱᧲᧳᧴᧵᧶᧷᧸᧹᧺᧻᧼᧽᧾᧿᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩" \
                    "᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᭡᭢᭣᭤᭥᭦᭧᭨᭩᭪᭴᭵᭶᭷᭸᭹᭺᭻᭼᯼᯽᯾᯿᰻᰼᰽᰾᰿᱾᱿᳀᳁᳂᳃᳄᳅᳆᳇᳓᾽᾿" \
                    "῀῁῍῎῏῝῞῟῭΅`´῾‐‑‒–—―‖‗‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›※‼‽‾‿⁀⁁" \
                    "⁂⁃⁄⁅⁆⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁒⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⁺⁻⁼⁽⁾₊₋₌₍₎₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯" \
                    "₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾℀℁℃℄℅℆℈℉℔№℗℘℞℟℠℡™℣℥℧℩℮℺℻⅀⅁⅂⅃⅄⅊" \
                    "⅋⅌⅍⅏↊↋←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭" \
                    "↮↯↰↱↲↳↴↵↶↷↸↹↺↻↼↽↾↿⇀⇁⇂⇃⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛⇜⇝⇞⇟⇠⇡⇢" \
                    "⇣⇤⇥⇦⇧⇨⇩⇪⇫⇬⇭⇮⇯⇰⇱⇲⇳⇴⇵⇶⇷⇸⇹⇺⇻⇼⇽⇾⇿∀∁∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘" \
                    "∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆≇≈≉≊≋" \
                    "≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾" \
                    "≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰" \
                    "⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘" \
                    "⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿⌀⌁" \
                    "⌂⌃⌄⌅⌆⌇⌈⌉⌊⌋⌌⌍⌎⌏⌐⌑⌒⌓⌔⌕⌖⌗⌘⌙⌚⌛⌜⌝⌞⌟⌠⌡⌢⌣⌤⌥⌦⌧⌨〈〉⌫⌬⌭⌮⌯⌰⌱⌲" \
                    "⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⌽⌾⌿⍀⍁⍂⍃⍄⍅⍆⍇⍈⍉⍊⍋⍌⍍⍎⍏⍐⍑⍒⍓⍔⍕⍖⍗⍘⍙⍚⍛⍜⍝⍞⍟⍠⍡⍢⍣⍤⍥⍦⍧⍨" \
                    "⍩⍪⍫⍬⍭⍮⍯⍰⍱⍲⍳⍴⍵⍶⍷⍸⍹⍺⍻⍼⍽⍾⍿⎀⎁⎂⎃⎄⎅⎆⎇⎈⎉⎊⎋⎌⎍⎎⎏⎐⎑⎒⎓⎔⎕⎖" \
                    "⎗⎘⎙⎚⎛⎜⎝⎞⎟⎠⎡⎢⎣⎤⎥⎦⎧⎨⎩⎪⎫⎬⎭⎮⎯⎰⎱⎲⎳⎴⎵⎶⎷⎸⎹⎺⎻⎼⎽⎾⎿⏀⏁⏂⏃⏄⏅" \
                    "⏆⏇⏈⏉⏊⏋⏌⏍⏎⏏⏐⏑⏒⏓⏔⏕⏖⏗⏘⏙⏚⏛⏜⏝⏞⏟⏠⏡⏢⏣⏤⏥⏦⏧⏨⏩⏪⏫⏬⏭⏮" \
                    "⏯⏰⏱⏲⏳⏴⏵⏶⏷⏸⏹⏺⏻⏼⏽⏾␀␁␂␃␄␅␆␇␈␉␊␋␌␍␎␏␐␑␒␓" \
                    "␔␕␖␗␘␙␚␛␜␝␞␟␠␡␢␣␤␥␦⑀⑁⑂⑃⑄⑅⑆⑇⑈⑉⑊⒜⒝⒞⒟⒠⒡⒢" \
                    "⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅ" \
                    "ⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧ" \
                    "ⓨⓩ─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰" \
                    "┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦" \
                    "╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝" \
                    "▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅◆◇◈◉◊○◌◍◎●◐◑◒◓" \
                    "◔◕◖◗◘◙◚◛◜◝◞◟◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯◰◱◲◳◴◵◶◷◸◹◺◻◼◽◾◿☀☁☂☃☄★☆☇☈☉☊" \
                    "☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯☰☱☲☳☴☵☶☷☸☹☺☻" \
                    "☼☽☾☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯" \
                    "♰♱♲♳♴♵♶♷♸♹♺♻♼♽♾♿⚀⚁⚂⚃⚄⚅⚆⚇⚈⚉⚊⚋⚌⚍⚎⚏⚐⚑⚒⚓⚔⚕⚖⚗⚘⚙⚚⚛⚜⚝⚞⚟⚠⚡" \
                    "⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯⚰⚱⚲⚳⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾⚿⛀⛁⛂⛃⛄⛅⛆⛇" \
                    "⛈⛉⛊⛋⛌⛍⛎⛏⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟⛠⛡⛢⛣⛤⛥⛦⛧⛨" \
                    "⛩⛪⛫⛬⛭⛮⛯⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿✀✁✂✃✄✅✆✇✈✉✊✋✌✍✎" \
                    "✏✐✑✒✓✔✕✖✗✘✙✚✛✜✝✞✟✠✡✢✣✤✥✦✧✨✩✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❄" \
                    "❅❆❇❈❉❊❋❌❍❎❏❐❑❒❓❔❕❖❗❘❙❚❛❜❝❞❟❠❡❢❣❤❥❦❧❨❩❪❫❬❭❮❯❰❱❲❳❴❵➔➕➖➗" \
                    "➘➙➚➛➜➝➞➟➠➡➢➣➤➥➦➧➨➩➪➫➬➭➮➯➰➱➲➳➴➵➶➷➸➹➺➻➼➽➾➿⟀⟁⟂⟃⟄⟅⟆⟇⟈" \
                    "⟉⟊⟋⟌⟍⟎⟏⟐⟑⟒⟓⟔⟕⟖⟗⟘⟙⟚⟛⟜⟝⟞⟟⟠⟡⟢⟣⟤⟥⟦⟧⟨⟩⟪⟫⟬⟭⟮⟯⟰⟱⟲⟳" \
                    "⟴⟵⟶⟷⟸⟹⟺⟻⟼⟽⟾⟿⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗" \
                    "⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄" \
                    "⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱" \
                    "⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝" \
                    "⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉" \
                    "⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶" \
                    "⣷⣸⣹⣺⣻⣼⣽⣾⣿⤀⤁⤂⤃⤄⤅⤆⤇⤈⤉⤊⤋⤌⤍⤎⤏⤐⤑⤒⤓⤔⤕⤖⤗⤘⤙⤚⤛⤜⤝" \
                    "⤞⤟⤠⤡⤢⤣⤤⤥⤦⤧⤨⤩⤪⤫⤬⤭⤮⤯⤰⤱⤲⤳⤴⤵⤶⤷⤸⤹⤺⤻⤼⤽⤾⤿⥀⥁⥂⥃" \
                    "⥄⥅⥆⥇⥈⥉⥊⥋⥌⥍⥎⥏⥐⥑⥒⥓⥔⥕⥖⥗⥘⥙⥚⥛⥜⥝⥞⥟⥠⥡⥢⥣⥤⥥⥦⥧⥨⥩" \
                    "⥪⥫⥬⥭⥮⥯⥰⥱⥲⥳⥴⥵⥶⥷⥸⥹⥺⥻⥼⥽⥾⥿⦀⦁⦂⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⦙⦚" \
                    "⦛⦜⦝⦞⦟⦠⦡⦢⦣⦤⦥⦦⦧⦨⦩⦪⦫⦬⦭⦮⦯⦰⦱⦲⦳⦴⦵⦶⦷⦸⦹⦺⦻⦼⦽⦾⦿⧀⧁⧂" \
                    "⧃⧄⧅⧆⧇⧈⧉⧊⧋⧌⧍⧎⧏⧐⧑⧒⧓⧔⧕⧖⧗⧘⧙⧚⧛⧜⧝⧞⧟⧠⧡⧢⧣⧤⧥⧦⧧⧨⧩" \
                    "⧪⧫⧬⧭⧮⧯⧰⧱⧲⧳⧴⧵⧶⧷⧸⧹⧺⧻⧼⧽⧾⧿⨀⨁⨂⨃⨄⨅⨆⨇⨈⨉⨊⨋⨌⨍⨎⨏⨐⨑⨒⨓⨔⨕⨖⨗⨘⨙⨚⨛" \
                    "⨜⨝⨞⨟⨠⨡⨢⨣⨤⨥⨦⨧⨨⨩⨪⨫⨬⨭⨮⨯⨰⨱⨲⨳⨴⨵⨶⨷⨸⨹⨺⨻⨼⨽⨾⨿⩀⩁⩂⩃⩄⩅" \
                    "⩆⩇⩈⩉⩊⩋⩌⩍⩎⩏⩐⩑⩒⩓⩔⩕⩖⩗⩘⩙⩚⩛⩜⩝⩞⩟⩠⩡⩢⩣⩤⩥⩦⩧⩨⩩⩪⩫⩬⩭⩮⩯" \
                    "⩰⩱⩲⩳⩴⩵⩶⩷⩸⩹⩺⩻⩼⩽⩾⩿⪀⪁⪂⪃⪄⪅⪆⪇⪈⪉⪊⪋⪌⪍⪎⪏⪐⪑⪒⪓" \
                    "⪔⪕⪖⪗⪘⪙⪚⪛⪜⪝⪞⪟⪠⪡⪢⪣⪤⪥⪦⪧⪨⪩⪪⪫⪬⪭⪮⪯⪰⪱⪲⪳⪴⪵⪶⪷" \
                    "⪸⪹⪺⪻⪼⪽⪾⪿⫀⫁⫂⫃⫄⫅⫆⫇⫈⫉⫊⫋⫌⫍⫎⫏⫐⫑⫒⫓⫔⫕⫖⫗⫘⫙⫚⫛⫝̸⫝⫞⫟⫠" \
                    "⫡⫢⫣⫤⫥⫦⫧⫨⫩⫪⫫⫬⫭⫮⫯⫰⫱⫲⫳⫴⫵⫶⫷⫸⫹⫺⫻⫼⫽⫾⫿⬀⬁⬂⬃⬄⬅⬆⬇⬈⬉⬊⬋⬌⬍⬎" \
                    "⬏⬐⬑⬒⬓⬔⬕⬖⬗⬘⬙⬚⬛⬜⬝⬞⬟⬠⬡⬢⬣⬤⬥⬦⬧⬨⬩⬪⬫⬬⬭⬮⬯⬰⬱⬲⬳⬴⬵⬶⬷⬸" \
                    "⬹⬺⬻⬼⬽⬾⬿⭀⭁⭂⭃⭄⭅⭆⭇⭈⭉⭊⭋⭌⭍⭎⭏⭐⭑⭒⭓⭔⭕⭖⭗⭘⭙⭚⭛" \
                    "⭜⭝⭞⭟⭠⭡⭢⭣⭤⭥⭦⭧⭨⭩⭪⭫⭬⭭⭮⭯⭰⭱⭲⭳⭶⭷⭸⭹⭺⭻⭼⭽⭾⭿⮀⮁⮂⮃⮄⮅⮆⮇" \
                    "⮈⮉⮊⮋⮌⮍⮎⮏⮐⮑⮒⮓⮔⮕⮘⮙⮚⮛⮜⮝⮞⮟⮠⮡⮢⮣⮤⮥⮦⮧⮨⮩⮪⮫⮬⮭⮮⮯⮰" \
                    "⮱⮲⮳⮴⮵⮶⮷⮸⮹⮽⮾⮿⯀⯁⯂⯃⯄⯅⯆⯇⯈⯊⯋⯌⯍⯎⯏⯐⯑⯬⯭⯮⯯⳥⳦⳧⳨⳩⳪⳹⳺" \
                    "⳻⳼⳾⳿⵰⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸓⸔⸕⸖⸗⸘⸙⸚⸛⸜⸝⸞⸟⸠⸡⸢⸣⸤⸥⸦⸧⸨⸩⸪⸫⸬⸭⸮⸰⸱⸲" \
                    "⸳⸴⸵⸶⸷⸸⸹⸺⸻⸼⸽⸾⸿⹀⹁⹂⹃⹄⺀⺁⺂⺃⺄⺅⺆⺇⺈⺉⺊⺋⺌⺍⺎⺏⺐⺑⺒⺓⺔" \
                    "⺕⺖⺗⺘⺙⺛⺜⺝⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵" \
                    "⺶⺷⺸⺹⺺⺻⺼⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕" \
                    "⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂" \
                    "⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣" \
                    "⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄" \
                    "⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦" \
                    "⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈" \
                    "⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪" \
                    "⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋" \
                    "⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻、。〃〄〈〉《》「」" \
                    "『』【】〒〓〔〕〖〗〘〙〚〛〜〝〞〟〠〰〶〷〽〾〿゛゜゠・㆐㆑㆖㆗㆘㆙㆚㆛" \
                    "㆜㆝㆞㆟㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛" \
                    "㇜㇝㇞㇟㇠㇡㇢㇣㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙" \
                    "㈚㈛㈜㈝㈞㈪㈫㈬㈭㈮㈯㈰㈱㈲㈳㈴㈵㈶㈷㈸㈹㈺㈻㈼㈽㈾㈿㉀㉁㉂㉃㉄" \
                    "㉅㉆㉇㉐㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㉼" \
                    "㉽㉾㉿㊊㊋㊌㊍㊎㊏㊐㊑㊒㊓㊔㊕㊖㊗㊘㊙㊚㊛㊜㊝㊞㊟㊠㊡㊢㊣㊤㊥㊦㊧" \
                    "㊨㊩㊪㊫㊬㊭㊮㊯㊰㋀㋁㋂㋃㋄㋅㋆㋇㋈㋉㋊㋋㋌㋍㋎㋏㋐㋑㋒㋓㋔㋕㋖㋗" \
                    "㋘㋙㋚㋛㋜㋝㋞㋟㋠㋡㋢㋣㋤㋥㋦㋧㋨㋩㋪㋫㋬㋭㋮㋯㋰㋱㋲㋳㋴㋵㋶㋷" \
                    "㋸㋹㋺㋻㋼㋽㋾㌀㌁㌂㌃㌄㌅㌆㌇㌈㌉㌊㌋㌌㌍㌎㌏㌐㌑㌒㌓㌔㌕㌖㌗㌘㌙" \
                    "㌚㌛㌜㌝㌞㌟㌠㌡㌢㌣㌤㌥㌦㌧㌨㌩㌪㌫㌬㌭㌮㌯㌰㌱㌲㌳㌴㌵㌶㌷㌸㌹" \
                    "㌺㌻㌼㌽㌾㌿㍀㍁㍂㍃㍄㍅㍆㍇㍈㍉㍊㍋㍌㍍㍎㍏㍐㍑㍒㍓㍔㍕㍖㍗㍘㍙㍚" \
                    "㍛㍜㍝㍞㍟㍠㍡㍢㍣㍤㍥㍦㍧㍨㍩㍪㍫㍬㍭㍮㍯㍰㍱㍲㍳㍴㍵㍶㍷㍸㍹㍺" \
                    "㍻㍼㍽㍾㍿㎀㎁㎂㎃㎄㎅㎆㎇㎈㎉㎊㎋㎌㎍㎎㎏㎐㎑㎒㎓㎔㎕㎖㎗㎘㎙㎚㎛㎜" \
                    "㎝㎞㎟㎠㎡㎢㎣㎤㎥㎦㎧㎨㎩㎪㎫㎬㎭㎮㎯㎰㎱㎲㎳㎴㎵㎶㎷㎸㎹㎺㎻㎼㎽㎾" \
                    "㎿㏀㏁㏂㏃㏄㏅㏆㏇㏈㏉㏊㏋㏌㏍㏎㏏㏐㏑㏒㏓㏔㏕㏖㏗㏘㏙㏚㏛㏜㏝㏞㏟㏠" \
                    "㏡㏢㏣㏤㏥㏦㏧㏨㏩㏪㏫㏬㏭㏮㏯㏰㏱㏲㏳㏴㏵㏶㏷㏸㏹㏺㏻㏼㏽㏾㏿䷀" \
                    "䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥" \
                    "䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿꒐꒑꒒꒓꒔꒕꒖꒗꒘꒙꒚꒛꒜꒝꒞꒟꒠" \
                    "꒡꒢꒣꒤꒥꒦꒧꒨꒩꒪꒫꒬꒭꒮꒯꒰꒱꒲꒳꒴꒵꒶꒷꒸꒹꒺꒻꒼꒽꒾꒿꓀꓁꓂꓃꓄꓅꓆꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷" \
                    "꜀꜁꜂꜃꜄꜅꜆꜇꜈꜉꜊꜋꜌꜍꜎꜏꜐꜑꜒꜓꜔꜕꜖꜠꜡꞉꞊꠨꠩꠪꠫꠶꠷꠸꠹꡴꡵꡶꡷꣎꣏꣸꣹꣺꣼꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇" \
                    "꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꩷꩸꩹꫞꫟꫰꫱꭛꯫﬩﮲﮳﮴﮵﮶﮷﮸﮹﮺﮻﮼﮽﮾﮿﯀﯁﴾﴿﷼﷽︐︑︒︓︔︕︖︗︘︙︰︱︲" \
                    "︳︴︵︶︷︸︹︺︻︼︽︾︿﹀﹁﹂﹃﹄﹅﹆﹇﹈﹉﹊﹋﹌﹍﹎﹏﹐﹑﹒" \
                    "﹔﹕﹖﹗﹘﹙﹚﹛﹜﹝﹞﹟﹠﹡﹢﹣﹤﹥﹦﹨﹩﹪﹫！＂＃＄％＆＇（）" \
                    "＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～｟｠｡｢｣､･￠￡￢￣￤" \
                    "￥￦￨￩￪￫￬￭￮￼�𐄀𐄁𐄂𐄷𐄸𐄹𐄺𐄻𐄼𐄽𐄾𐄿𐅹𐅺𐅻𐅼𐅽𐅾𐅿𐆀𐆁𐆂𐆃𐆄𐆅𐆆𐆇𐆈𐆉𐆌𐆍𐆎𐆐𐆑𐆒𐆓𐆔𐆕𐆖𐆗𐆘" \
                    "𐆙𐆚𐆛𐆠𐇐𐇑𐇒𐇓𐇔𐇕𐇖𐇗𐇘𐇙𐇚𐇛𐇜𐇝𐇞𐇟𐇠𐇡𐇢𐇣𐇤𐇥𐇦𐇧𐇨𐇩𐇪𐇫𐇬𐇭𐇮𐇯𐇰𐇱𐇲𐇳𐇴𐇵𐇶𐇷𐇸𐇹𐇺𐇻𐇼𐎟𐏐" \
                    "𐕯𐡗𐡷𐡸𐤟𐤿𐩐𐩑𐩒𐩓𐩔𐩕𐩖𐩗𐩘𐩿𐫈𐫰𐫱𐫲𐫳𐫴𐫵𐫶𐬹𐬺𐬻𐬼𐬽𐬾𐬿𐮙𐮚𐮛𐮜𑁇𑁈𑁉𑁊𑁋𑁌𑁍𑂻𑂼𑂾𑂿𑃀𑃁𑅀𑅁𑅂𑅃𑅴" \
                    "𑅵𑇅𑇆𑇇𑇈𑇉𑇍𑇛𑇝𑇞𑇟𑈸𑈹𑈺𑈻𑈼𑈽𑊩𑑋𑑌𑑍𑑎𑑏𑑛𑑝𑓆𑗁𑗂𑗃𑗄𑗅𑗆𑗇𑗈𑗉𑗊𑗋𑗌𑗍𑗎𑗏𑗐𑗑𑗒𑗓𑗔𑗕𑗖𑗗𑙁𑙂𑙃𑙠𑙡" \
                    "𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬𑜼𑜽𑜾𑜿𑱁𑱂𑱃𑱄𑱅𑱰𑱱𒑰𒑱𒑲𒑳𒑴𖩮𖩯𖫵𖬷𖬸𖬹𖬺𖬻𖬼𖬽𖬾𖬿𖭄𖭅𛲜𛲟𝀀𝀁𝀂𝀃𝀄𝀅𝀆𝀇𝀈𝀉" \
                    "𝀊𝀋𝀌𝀍𝀎𝀏𝀐𝀑𝀒𝀓𝀔𝀕𝀖𝀗𝀘𝀙𝀚𝀛𝀜𝀝𝀞𝀟𝀠𝀡𝀢𝀣𝀤𝀥𝀦𝀧𝀨𝀩𝀪𝀫𝀬𝀭𝀮𝀯𝀰𝀱𝀲𝀳𝀴𝀵𝀶𝀷𝀸𝀹𝀺𝀻𝀼𝀽" \
                    "𝀾𝀿𝁀𝁁𝁂𝁃𝁄𝁅𝁆𝁇𝁈𝁉𝁊𝁋𝁌𝁍𝁎𝁏𝁐𝁑𝁒𝁓𝁔𝁕𝁖𝁗𝁘𝁙𝁚𝁛𝁜𝁝𝁞𝁟𝁠𝁡𝁢𝁣𝁤𝁥𝁦𝁧" \
                    "𝁨𝁩𝁪𝁫𝁬𝁭𝁮𝁯𝁰𝁱𝁲𝁳𝁴𝁵𝁶𝁷𝁸𝁹𝁺𝁻𝁼𝁽𝁾𝁿𝂀𝂁𝂂𝂃𝂄𝂅𝂆𝂇𝂈𝂉𝂊𝂋𝂌𝂍𝂎𝂏𝂐" \
                    "𝂑𝂒𝂓𝂔𝂕𝂖𝂗𝂘𝂙𝂚𝂛𝂜𝂝𝂞𝂟𝂠𝂡𝂢𝂣𝂤𝂥𝂦𝂧𝂨𝂩𝂪𝂫𝂬𝂭𝂮𝂯𝂰𝂱𝂲𝂳𝂴𝂵𝂶𝂷𝂸𝂹𝂺𝂻𝂼𝂽𝂾𝂿𝃀𝃁𝃂𝃃𝃄" \
                    "𝃅𝃆𝃇𝃈𝃉𝃊𝃋𝃌𝃍𝃎𝃏𝃐𝃑𝃒𝃓𝃔𝃕𝃖𝃗𝃘𝃙𝃚𝃛𝃜𝃝𝃞𝃟𝃠𝃡𝃢𝃣𝃤𝃥𝃦𝃧𝃨𝃩𝃪𝃫𝃬𝃭𝃮𝃯𝃰𝃱𝃲𝃳𝃴𝃵" \
                    "𝄀𝄁𝄂𝄃𝄄𝄅𝄆𝄇𝄈𝄉𝄊𝄋𝄌𝄍𝄎𝄏𝄐𝄑𝄒𝄓𝄔𝄕𝄖𝄗𝄘𝄙𝄚𝄛𝄜𝄝𝄞𝄟𝄠𝄡𝄢𝄣𝄤𝄥𝄦𝄩𝄪𝄫𝄬𝄭𝄮𝄯𝄰𝄱" \
                    "𝄲𝄳𝄴𝄵𝄶𝄷𝄸𝄹𝄺𝄻𝄼𝄽𝄾𝄿𝅀𝅁𝅂𝅃𝅄𝅅𝅆𝅇𝅈𝅉𝅊𝅋𝅌𝅍𝅎𝅏𝅐𝅑𝅒𝅓𝅔𝅕𝅖𝅗𝅘𝅙𝅚𝅛𝅜𝅝𝅗𝅥𝅘𝅥𝅘𝅥𝅮𝅘𝅥𝅯𝅘𝅥𝅰𝅘𝅥𝅱𝅘𝅥𝅲𝅪𝅫" \
                    "𝅬𝆃𝆄𝆌𝆍𝆎𝆏𝆐𝆑𝆒𝆓𝆔𝆕𝆖𝆗𝆘𝆙𝆚𝆛𝆜𝆝𝆞𝆟𝆠𝆡𝆢𝆣𝆤𝆥𝆦𝆧𝆨𝆩𝆮𝆯𝆰𝆱𝆲𝆳𝆴𝆵𝆶𝆷𝆸𝆹𝆺𝆹𝅥𝆺𝅥𝆹𝅥𝅮𝆺𝅥𝅮" \
                    "𝆹𝅥𝅯𝆺𝅥𝅯𝇁𝇂𝇃𝇄𝇅𝇆𝇇𝇈𝇉𝇊𝇋𝇌𝇍𝇎𝇏𝇐𝇑𝇒𝇓𝇔𝇕𝇖𝇗𝇘𝇙𝇚𝇛𝇜𝇝𝇞𝇟𝇠𝇡𝇢𝇣𝇤𝇥𝇦𝇧𝇨𝈀𝈁𝈂𝈃𝈄𝈅𝈆𝈇𝈈𝈉𝈊" \
                    "𝈋𝈌𝈍𝈎𝈏𝈐𝈑𝈒𝈓𝈔𝈕𝈖𝈗𝈘𝈙𝈚𝈛𝈜𝈝𝈞𝈟𝈠𝈡𝈢𝈣𝈤𝈥𝈦𝈧𝈨𝈩𝈪𝈫𝈬𝈭𝈮𝈯𝈰𝈱𝈲𝈳𝈴𝈵𝈶𝈷" \
                    "𝈸𝈹𝈺𝈻𝈼𝈽𝈾𝈿𝉀𝉁𝉅𝌀𝌁𝌂𝌃𝌄𝌅𝌆𝌇𝌈𝌉𝌊𝌋𝌌𝌍𝌎𝌏𝌐𝌑𝌒𝌓𝌔𝌕𝌖𝌗𝌘𝌙𝌚" \
                    "𝌛𝌜𝌝𝌞𝌟𝌠𝌡𝌢𝌣𝌤𝌥𝌦𝌧𝌨𝌩𝌪𝌫𝌬𝌭𝌮𝌯𝌰𝌱𝌲𝌳𝌴𝌵𝌶𝌷𝌸𝌹𝌺𝌻𝌼𝌽𝌾𝌿" \
                    "𝍀𝍁𝍂𝍃𝍄𝍅𝍆𝍇𝍈𝍉𝍊𝍋𝍌𝍍𝍎𝍏𝍐𝍑𝍒𝍓𝍔𝍕𝍖𝛁𝛛𝛻𝜕𝜵𝝏𝝯𝞉𝞩𝟃𝠀𝠁𝠂𝠃𝠄𝠅𝠆𝠇𝠈𝠉" \
                    "𝠊𝠋𝠌𝠍𝠎𝠏𝠐𝠑𝠒𝠓𝠔𝠕𝠖𝠗𝠘𝠙𝠚𝠛𝠜𝠝𝠞𝠟𝠠𝠡𝠢𝠣𝠤𝠥𝠦𝠧𝠨𝠩𝠪𝠫𝠬𝠭𝠮𝠯𝠰𝠱𝠲𝠳𝠴𝠵𝠶𝠷𝠸𝠹𝠺𝠻𝠼𝠽𝠾" \
                    "𝠿𝡀𝡁𝡂𝡃𝡄𝡅𝡆𝡇𝡈𝡉𝡊𝡋𝡌𝡍𝡎𝡏𝡐𝡑𝡒𝡓𝡔𝡕𝡖𝡗𝡘𝡙𝡚𝡛𝡜𝡝𝡞𝡟𝡠𝡡𝡢𝡣𝡤𝡥𝡦𝡧𝡨𝡩𝡪𝡫𝡬𝡭𝡮𝡯𝡰𝡱𝡲𝡳𝡴𝡵" \
                    "𝡶𝡷𝡸𝡹𝡺𝡻𝡼𝡽𝡾𝡿𝢀𝢁𝢂𝢃𝢄𝢅𝢆𝢇𝢈𝢉𝢊𝢋𝢌𝢍𝢎𝢏𝢐𝢑𝢒𝢓𝢔𝢕𝢖𝢗𝢘𝢙𝢚𝢛𝢜𝢝𝢞𝢟𝢠𝢡𝢢𝢣𝢤𝢥𝢦𝢧𝢨𝢩𝢪" \
                    "𝢫𝢬𝢭𝢮𝢯𝢰𝢱𝢲𝢳𝢴𝢵𝢶𝢷𝢸𝢹𝢺𝢻𝢼𝢽𝢾𝢿𝣀𝣁𝣂𝣃𝣄𝣅𝣆𝣇𝣈𝣉𝣊𝣋𝣌𝣍𝣎𝣏𝣐𝣑𝣒𝣓𝣔𝣕𝣖𝣗𝣘𝣙𝣚𝣛𝣜𝣝𝣞𝣟𝣠" \
                    "𝣡𝣢𝣣𝣤𝣥𝣦𝣧𝣨𝣩𝣪𝣫𝣬𝣭𝣮𝣯𝣰𝣱𝣲𝣳𝣴𝣵𝣶𝣷𝣸𝣹𝣺𝣻𝣼𝣽𝣾𝣿𝤀𝤁𝤂𝤃𝤄𝤅𝤆𝤇𝤈𝤉𝤊𝤋𝤌𝤍𝤎𝤏𝤐𝤑𝤒𝤓𝤔𝤕𝤖" \
                    "𝤗𝤘𝤙𝤚𝤛𝤜𝤝𝤞𝤟𝤠𝤡𝤢𝤣𝤤𝤥𝤦𝤧𝤨𝤩𝤪𝤫𝤬𝤭𝤮𝤯𝤰𝤱𝤲𝤳𝤴𝤵𝤶𝤷𝤸𝤹𝤺𝤻𝤼𝤽𝤾𝤿𝥀𝥁𝥂𝥃𝥄𝥅𝥆𝥇𝥈𝥉𝥊𝥋𝥌" \
                    "𝥍𝥎𝥏𝥐𝥑𝥒𝥓𝥔𝥕𝥖𝥗𝥘𝥙𝥚𝥛𝥜𝥝𝥞𝥟𝥠𝥡𝥢𝥣𝥤𝥥𝥦𝥧𝥨𝥩𝥪𝥫𝥬𝥭𝥮𝥯𝥰𝥱𝥲𝥳𝥴𝥵𝥶𝥷𝥸𝥹𝥺𝥻𝥼𝥽𝥾𝥿𝦀𝦁𝦂𝦃" \
                    "𝦄𝦅𝦆𝦇𝦈𝦉𝦊𝦋𝦌𝦍𝦎𝦏𝦐𝦑𝦒𝦓𝦔𝦕𝦖𝦗𝦘𝦙𝦚𝦛𝦜𝦝𝦞𝦟𝦠𝦡𝦢𝦣𝦤𝦥𝦦𝦧𝦨𝦩𝦪𝦫𝦬𝦭𝦮𝦯𝦰𝦱𝦲𝦳𝦴𝦵𝦶𝦷𝦸𝦹𝦺" \
                    "𝦻𝦼𝦽𝦾𝦿𝧀𝧁𝧂𝧃𝧄𝧅𝧆𝧇𝧈𝧉𝧊𝧋𝧌𝧍𝧎𝧏𝧐𝧑𝧒𝧓𝧔𝧕𝧖𝧗𝧘𝧙𝧚𝧛𝧜𝧝𝧞𝧟𝧠𝧡𝧢𝧣𝧤𝧥𝧦𝧧𝧨𝧩𝧪𝧫𝧬𝧭𝧮𝧯𝧰" \
                    "𝧱𝧲𝧳𝧴𝧵𝧶𝧷𝧸𝧹𝧺𝧻𝧼𝧽𝧾𝧿𝨷𝨸𝨹𝨺𝩭𝩮𝩯𝩰𝩱𝩲𝩳𝩴𝩶𝩷𝩸𝩹𝩺𝩻𝩼𝩽𝩾𝩿𝪀𝪁𝪂𝪃𝪅𝪆𝪇𝪈𝪉𝪊𝪋𞥞𞥟𞻰𞻱🀀🀁" \
                    "🀂🀃🀄🀅🀆🀇🀈🀉🀊🀋🀌🀍🀎🀏🀐🀑🀒🀓🀔🀕🀖🀗🀘🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣🀤🀥🀦🀧🀨🀩" \
                    "🀪🀫🀰🀱🀲🀳🀴🀵🀶🀷🀸🀹🀺🀻🀼🀽🀾🀿🁀🁁🁂🁃🁄🁅🁆" \
                    "🁇🁈🁉🁊🁋🁌🁍🁎🁏🁐🁑🁒🁓🁔🁕🁖🁗🁘🁙🁚🁛🁜🁝🁞🁟" \
                    "🁠🁡🁢🁣🁤🁥🁦🁧🁨🁩🁪🁫🁬🁭🁮🁯🁰🁱🁲🁳🁴🁵🁶🁷🁸🁹🁺🁻🁼🁽🁾🁿🂀🂁🂂🂃🂄🂅🂆" \
                    "🂇🂈🂉🂊🂋🂌🂍🂎🂏🂐🂑🂒🂓🂠🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂬🂭🂮🂱🂲🂳🂴🂵🂶🂷🂸" \
                    "🂹🂺🂻🂼🂽🂾🂿🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃌🃍🃎🃏🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚" \
                    "🃛🃜🃝🃞🃟🃠🃡🃢🃣🃤🃥🃦🃧🃨🃩🃪🃫🃬🃭🃮🃯🃰🃱🃲🃳🃴🃵🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙" \
                    "🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩🄪🄫🄬🄭🄮🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻" \
                    "🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅊🅋🅌🅍🅎🅏🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛" \
                    "🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅪🅫🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀" \
                    "🆁🆂🆃🆄🆅🆆🆇🆈🆉🆊🆋🆌🆍🆎🆏🆐🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🆛🆜🆝🆞🆟🆠🆡🆢🆣🆤" \
                    "🆥🆦🆧🆨🆩🆪🆫🆬🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🈀🈁" \
                    "🈂🈐🈑🈒🈓🈔🈕🈖🈗🈘🈙🈚🈛🈜🈝🈞🈟🈠🈡🈢🈣🈤🈥🈦🈧🈨🈩🈪🈫🈬🈭🈮" \
                    "🈯🈰🈱🈲🈳🈴🈵🈶🈷🈸🈹🈺🈻🉀🉁🉂🉃🉄🉅🉆🉇🉈🉐🉑🌀🌁🌂🌃🌄🌅🌆🌇" \
                    "🌈🌉🌊🌋🌌🌍🌎🌏🌐🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜🌝🌞🌟🌠🌡🌢🌣🌤🌥🌦🌧🌨🌩🌪" \
                    "🌫🌬🌭🌮🌯🌰🌱🌲🌳🌴🌵🌶🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍" \
                    "🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰" \
                    "🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼🍽🍾🍿🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎔" \
                    "🎕🎖🎗🎘🎙🎚🎛🎜🎝🎞🎟🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷" \
                    "🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏃🏄🏅🏆🏇🏈🏉🏊🏋🏌🏍🏎🏏🏐🏑🏒🏓🏔🏕🏖🏗🏘🏙🏚" \
                    "🏛🏜🏝🏞🏟🏠🏡🏢🏣🏤🏥🏦🏧🏨🏩🏪🏫🏬🏭🏮🏯🏰🏱🏲🏳🏴🏵🏶🏷🏸🏹🏺🏻🏼" \
                    "🏽🏾🏿🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝" \
                    "🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾" \
                    "🐿👀👁👂👃👄👅👆👇👈👉👊👋👌👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢" \
                    "👣👤👥👦👧👨👩👪👫👬👭👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄💅" \
                    "💆💇💈💉💊💋💌💍💎💏💐💑💒💓💔💕💖💗💘💙💚💛💜💝💞💟💠💡💢💣💤💥💦" \
                    "💧💨💩💪💫💬💭💮💯💰💱💲💳💴💵💶💷💸💹💺💻💼💽💾💿📀📁📂📃📄📅📆📇📈" \
                    "📉📊📋📌📍📎📏📐📑📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨📩" \
                    "📪📫📬📭📮📯📰📱📲📳📴📵📶📷📸📹📺📻📼📽📾📿🔀🔁🔂🔃🔄🔅🔆🔇🔈🔉🔊🔋🔌🔍🔎" \
                    "🔏🔐🔑🔒🔓🔔🔕🔖🔗🔘🔙🔚🔛🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫🔬🔭🔮🔯🔰🔱" \
                    "🔲🔳🔴🔵🔶🔷🔸🔹🔺🔻🔼🔽🔾🔿🕀🕁🕂🕃🕄🕅🕆🕇🕈🕉🕊🕋🕌🕍🕎🕏🕐🕑🕒🕓🕔🕕🕖" \
                    "🕗🕘🕙🕚🕛🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧🕨🕩🕪🕫🕬🕭🕮🕯🕰🕱🕲🕳🕴🕵🕶🕷🕸🕹🕺" \
                    "🕻🕼🕽🕾🕿🖀🖁🖂🖃🖄🖅🖆🖇🖈🖉🖊🖋🖌🖍🖎🖏🖐🖑🖒🖓🖔🖕🖖🖗🖘🖙🖚🖛🖜🖝🖞🖟🖠🖡" \
                    "🖢🖣🖤🖥🖦🖧🖨🖩🖪🖫🖬🖭🖮🖯🖰🖱🖲🖳🖴🖵🖶🖷🖸🖹🖺🖻🖼🖽🖾🖿🗀🗁🗂🗃🗄🗅" \
                    "🗆🗇🗈🗉🗊🗋🗌🗍🗎🗏🗐🗑🗒🗓🗔🗕🗖🗗🗘🗙🗚🗛🗜🗝🗞🗟🗠🗡🗢🗣🗤🗥🗦🗧🗨" \
                    "🗩🗪🗫🗬🗭🗮🗯🗰🗱🗲🗳🗴🗵🗶🗷🗸🗹🗺🗻🗼🗽🗾🗿😀😁😂😃😄😅😆😇😈😉" \
                    "😊😋😌😍😎😏😐😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟😠😡😢😣😤😥😦😧" \
                    "😨😩😪😫😬😭😮😯😰😱😲😳😴😵😶😷😸😹😺😻😼😽😾😿🙀🙁🙂🙃🙄🙅" \
                    "🙆🙇🙈🙉🙊🙋🙌🙍🙎🙏🙐🙑🙒🙓🙔🙕🙖🙗🙘🙙🙚🙛🙜🙝🙞🙟🙠🙡🙢🙣🙤🙥🙦" \
                    "🙧🙨🙩🙪🙫🙬🙭🙮🙯🙰🙱🙲🙳🙴🙵🙶🙷🙸🙹🙺🙻🙼🙽🙾🙿🚀🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊🚋" \
                    "🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🚚🚛🚜🚝🚞🚟🚠🚡🚢🚣🚤🚥🚦🚧🚨🚩🚪🚫🚬🚭🚮" \
                    "🚯🚰🚱🚲🚳🚴🚵🚶🚷🚸🚹🚺🚻🚼🚽🚾🚿🛀🛁🛂🛃🛄🛅🛆🛇🛈🛉🛊🛋🛌🛍🛎🛏🛐🛑🛒🛠🛡🛢" \
                    "🛣🛤🛥🛦🛧🛨🛩🛪🛫🛬🛰🛱🛲🛳🛴🛵🛶🜀🜁🜂🜃🜄🜅🜆🜇🜈🜉🜊🜋🜌🜍🜎🜏🜐🜑🜒🜓🜔" \
                    "🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭🜮🜯🜰🜱🜲🜳🜴🜵🜶🜷🜸🜹🜺🜻🜼🜽🜾🜿🝀🝁🝂🝃🝄" \
                    "🝅🝆🝇🝈🝉🝊🝋🝌🝍🝎🝏🝐🝑🝒🝓🝔🝕🝖🝗🝘🝙🝚🝛🝜🝝🝞🝟🝠🝡🝢🝣🝤🝥🝦🝧🝨🝩🝪🝫🝬🝭🝮🝯" \
                    "🝰🝱🝲🝳🞀🞁🞂🞃🞄🞅🞆🞇🞈🞉🞊🞋🞌🞍🞎🞏🞐🞑🞒🞓🞔🞕🞖🞗🞘🞙🞚🞛🞜🞝🞞🞟🞠🞡🞢🞣🞤🞥🞦" \
                    "🞧🞨🞩🞪🞫🞬🞭🞮🞯🞰🞱🞲🞳🞴🞵🞶🞷🞸🞹🞺🞻🞼🞽🞾🞿🟀🟁🟂🟃🟄🟅🟆🟇🟈🟉🟊🟋🟌" \
                    "🟍🟎🟏🟐🟑🟒🟓🟔🠀🠁🠂🠃🠄🠅🠆🠇🠈🠉🠊🠋🠐🠑🠒🠓🠔🠕🠖🠗🠘🠙🠚🠛🠜🠝🠞🠟🠠🠡🠢🠣🠤🠥🠦" \
                    "🠧🠨🠩🠪🠫🠬🠭🠮🠯🠰🠱🠲🠳🠴🠵🠶🠷🠸🠹🠺🠻🠼🠽🠾🠿🡀🡁🡂🡃🡄🡅🡆🡇🡐🡑🡒🡓🡔🡕🡖🡗🡘🡙🡠🡡🡢" \
                    "🡣🡤🡥🡦🡧🡨🡩🡪🡫🡬🡭🡮🡯🡰🡱🡲🡳🡴🡵🡶🡷🡸🡹🡺🡻🡼🡽🡾🡿🢀🢁🢂🢃🢄🢅🢆🢇🢐🢑" \
                    "🢒🢓🢔🢕🢖🢗🢘🢙🢚🢛🢜🢝🢞🢟🢠🢡🢢🢣🢤🢥🢦🢧🢨🢩🢪🢫🢬🢭🤐🤑🤒🤓🤔🤕🤖🤗🤘🤙🤚🤛🤜🤝🤞🤠" \
                    "🤡🤢🤣🤤🤥🤦🤧🤰🤳🤴🤵🤶🤷🤸🤹🤺🤻🤼🤽🤾🥀🥁🥂🥃🥄🥅🥆🥇🥈🥉🥊🥋🥐🥑🥒🥓🥔🥕🥖🥗🥘🥙🥚🥛🥜🥝🥞🦀🦁🦂🦃" \
                    "🦄🦅🦆🦇🦈🦉🦊🦋🦌🦍🦎🦏🦐🦑🧀 "
