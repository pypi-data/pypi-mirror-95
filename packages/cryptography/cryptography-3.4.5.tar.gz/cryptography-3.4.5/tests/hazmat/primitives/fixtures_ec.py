# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.


from cryptography.hazmat.primitives.asymmetric import ec


EC_KEY_SECT571R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "213997069697108634621868251335076179190383272087548888968788698953"
        "131928375431570122753130054966269038244076049869476736547896549201"
        "7388482714521707824160638375437887802901"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT571R1(),
        x=int(
            "42585672410900520895287019432267514156432686681290164230262278"
            "54789182447139054594501570747809649335533486119017169439209005"
            "883737780433424425566023654583165324498640038089"
        ),
        y=int(
            "13822523320209387572500458104799806851658024537477228250738334"
            "46977851514777531296572763848253279034733550774927720436494321"
            "97281333379623823457479233585424800362717541750"
        ),
    ),
)

EC_KEY_SECT409R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "604993237916498765317587097853603474519114726157206838874832379003"
        "281871982139714656205843929472002062791572217653118715727"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT409R1(),
        x=int(
            "76237701339268928039087238870073679814646664010783544301589269"
            "2272579213400205907766385199643053767195204247826349822350081"
        ),
        y=int(
            "10056668929618383045204866060110626563392345494925302478351744"
            "01475129090774493235522729123877384838835703483224447476728811"
        ),
    ),
)

EC_KEY_SECT283R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "589705077255658434962118789801402573495547207239917043241273753671"
        "0603230261342427657"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT283R1(),
        x=int(
            "10694213430317013187241490088760888472172922291550831393222973"
            "531614941756901942108493"
        ),
        y=int(
            "11461553100313943515373601367527399649593366728262918214942116"
            "4359557613202950705170"
        ),
    ),
)

EC_KEY_SECT233R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "343470067105388144757135261232658742142830154753739648095101899829"
        "8288"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT233R1(),
        x=int(
            "74494951569151557692195071465128140646140765188698294062550374"
            "71118267"
        ),
        y=int(
            "48699150823022962508544923825876164485917001162461401797511748"
            "44872205"
        ),
    ),
)

EC_KEY_SECT163R2 = ec.EllipticCurvePrivateNumbers(
    private_value=int("11788436193853888218177032687141056784083668635"),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT163R2(),
        x=int("5247234453330640212490501030772203801908103222463"),
        y=int("3172513801099088785224248292142866317754124455206"),
    ),
)

EC_KEY_SECT571K1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "592811051234886966121888758661314648311634839499582476726008738218"
        "165015048237934517672316204181933804884636855291118594744334592153"
        "883208936227914544246799490897169723387"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT571K1(),
        x=int(
            "81362471461936552203898455874182916939857774872643607884250052"
            "29301336524105230729653881789373412990921493551253481866317181"
            "50644729351721577822595637058949405764944491655"
        ),
        y=int(
            "14058041260812945396067821061063618047896814719828637241661260"
            "31235681542401975593036630733881695595289523801041910183736211"
            "587294494888450327374439795428519848065589000434"
        ),
    ),
)

EC_KEY_SECT409K1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "110321743150399087059465162400463719641470113494908091197354523708"
        "934106732952992153105338671368548199643686444619485307877"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT409K1(),
        x=int(
            "62280214209410363493525178797944995742119600145953755916426161"
            "0790364158569265348038207313261547476506319796469776797725796"
        ),
        y=int(
            "46653883749102474289095010108777579907422472804577185369332018"
            "7318642669590280811057512951467298158275464566214288556375885"
        ),
    ),
)

EC_KEY_SECT283K1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "182508394415444014156574733141549331538128234395356466108310015130"
        "3868915489347291850"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT283K1(),
        x=int(
            "31141647206111886426350703123670451554123180910379592764773885"
            "2959123367428352287032"
        ),
        y=int(
            "71787460144483665964585187837283963089964760704065205376175384"
            "58957627834444017112582"
        ),
    ),
)

EC_KEY_SECT233K1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "172670089647474613734091436081960550801254775902629891892394471086"
        "2070"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT233K1(),
        x=int(
            "55693911474339510991521579392202889561373678973929426354737048"
            "68129172"
        ),
        y=int(
            "11025856248546376145959939911850923631416718241836051344384802"
            "737277815"
        ),
    ),
)

EC_KEY_SECT163K1 = ec.EllipticCurvePrivateNumbers(
    private_value=int("3699303791425402204035307605170569820290317991287"),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECT163K1(),
        x=int("4479755902310063321544063130576409926980094120721"),
        y=int("3051218481937171839039826690648109285113977745779"),
    ),
)

EC_KEY_SECP521R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "662751235215460886290293902658128847495347691199214706697089140769"
        "672273950767961331442265530524063943548846724348048614239791498442"
        "5997823106818915698960565"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECP521R1(),
        x=int(
            "12944742826257420846659527752683763193401384271391513286022917"
            "29910013082920512632908350502247952686156279140016049549948975"
            "670668730618745449113644014505462"
        ),
        y=int(
            "10784108810271976186737587749436295782985563640368689081052886"
            "16296815984553198866894145509329328086635278430266482551941240"
            "591605833440825557820439734509311"
        ),
    ),
)

EC_KEY_SECP384R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "280814107134858470598753916394807521398239633534281633982576099083"
        "35787109896602102090002196616273211495718603965098"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECP384R1(),
        x=int(
            "10036914308591746758780165503819213553101287571902957054148542"
            "504671046744460374996612408381962208627004841444205030"
        ),
        y=int(
            "17337335659928075994560513699823544906448896792102247714689323"
            "575406618073069185107088229463828921069465902299522926"
        ),
    ),
)

EC_KEY_SECP256R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "271032978511595617649844168316234344656921218699414461240502635010"
        "25776962849"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECP256R1(),
        x=int(
            "49325986169170464532722748935508337546545346352733747948730305"
            "442770101441241"
        ),
        y=int(
            "51709162888529903487188595007092772817469799707382623884187518"
            "455962250433661"
        ),
    ),
)

EC_KEY_SECP256K1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "683341569008473593765879222774207677458810362976327530563215318048"
        "64380736732"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECP256K1(),
        x=int(
            "59251322975795306609293064274738085741081547489119277536110995"
            "120127593127884"
        ),
        y=int(
            "10334192001480392039227801832201340147605940717841294644187071"
            "8261641142297801"
        ),
    ),
)

EC_KEY_SECP224R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "234854340492774342642505519082413233282383066880756900834047566251"
        "50"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECP224R1(),
        x=int(
            "51165676638271204691095081341581621487998422645261573824239666"
            "1214"
        ),
        y=int(
            "14936601450555711309158397172719963843891926209168533453717969"
            "1265"
        ),
    ),
)

EC_KEY_SECP192R1 = ec.EllipticCurvePrivateNumbers(
    private_value=int(
        "4534766128536179420071447168915990251715442361606049349869"
    ),
    public_numbers=ec.EllipticCurvePublicNumbers(
        curve=ec.SECP192R1(),
        x=int("5415069751170397888083674339683360671310515485781457536999"),
        y=int("18671605334415960797751252911958331304288357195986572776"),
    ),
)
