// @ts-ignore
import { Request, Response } from 'express';

export default {
  'GET /api/v1/component_change/:name/precheck': (req: Request, res: Response) => {
    res.status(200).send({
      code: 65,
      data: {
        total: 85,
        finished: 76,
        all_passed: true,
        status: {
          '0': 'S',
          '1': 'U',
          '2': 'C',
          '3': 'C',
          '4': 'E',
          '5': 'S',
          '6': 'S',
          '7': 'F',
          '8': 'U',
          '9': 'L',
        },
        message: '龙少先两资周群传法子又信行例气。',
        info: [
          {
            name: '段秀兰',
            server: '强划开里就就角个身产置人商相题空。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: true,
            code: '委口极解重代极心百油至花就。',
            description: '应究如温出出下市类权下毛好究设。',
            advisement: { description: '展常飞打细社接目县圆即在王。' },
          },
          {
            name: '蔡平',
            server: '口题分重活象直回部按利积如北热么。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: true,
            code: '阶了决果号角影利改当历间。',
            description: '育始没市常权此那又立半东此增向标。',
            advisement: { description: '入会名圆产实除术路好称约声。' },
          },
          {
            name: '邓刚',
            server: '对里技观龙积然多思空离十值。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '规斗当过一品标程验真位争九。',
            description: '式亲小保于除者下公只习开例。',
            advisement: { description: '社确八矿类资好能难商并性间表中。' },
          },
          {
            name: '黎刚',
            server: '技活次许他计便政毛完市建较如光内响。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '队非验节管图中保调可思期。',
            description: '特技带现业打没美心任专断由。',
            advisement: { description: '前动空造院求员发于历来义龙。' },
          },
          {
            name: '吕秀英',
            server: '位军便风变物六话土严分什声。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '支世周切间选单不五持各不林界已。',
            description: '科如北状级清对音强半极动京证前。',
            advisement: { description: '前期使干先系器代机及市已两所。' },
          },
          {
            name: '卢超',
            server: '被存世好音总那证给打局务断到。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '况查直列特县看样半花山毛那好完。',
            description: '内铁或南维县月即属己段自七条别正干。',
            advisement: { description: '前白然取至装器生温物装半周立放。' },
          },
          {
            name: '白艳',
            server: '我合矿称价维质书全社济照电织军研。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '目设志为用来拉物气变通共回也交形通。',
            description: '等定议增物做热价住步度术百领。',
            advisement: { description: '业结代她务因理果海做子水头。' },
          },
          {
            name: '潘秀英',
            server: '行儿导度如电世光图声多化上收须线织。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: true,
            code: '场二正何放委年风该收员界共意所。',
            description: '多增改变理和区设全容地直影常政。',
            advisement: { description: '众知其严学达石后引从交明提合作维南。' },
          },
          {
            name: '张芳',
            server: '市期包维展照目军及完就整县一。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: true,
            code: '极好两安始节九运意包空学高规。',
            description: '起育非何族成县放之更转他程。',
            advisement: { description: '准思传该层候算而离生使认近看完。' },
          },
          {
            name: '孙芳',
            server: '消参确用外群美总志连风化节存土才。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '影状可压对建步需具学写头生一。',
            description: '列完论成大观常金至九者设直问家已。',
            advisement: { description: '通然角书才真器化题各器候京便。' },
          },
          {
            name: '方伟',
            server: '军影器于包价面前好即头下。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '群会成置光构权调记又验单造所于。',
            description: '标响华生铁先价日年应世农百主半当引。',
            advisement: { description: '每织效此是整技大提单行识。' },
          },
          {
            name: '孔芳',
            server: '和深体期合代深中织率何率原。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: true,
            code: '采步革用有龙常外劳好想难到龙。',
            description: '难话列了群四下发你五布光照号张地重。',
            advisement: { description: '用利设团始至段车其就即调你。' },
          },
          {
            name: '潘艳',
            server: '对生者区料成头世易周听格效认。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '次建者率关写家影前圆交识段说信任知。',
            description: '会规都都文分就权格强土现层。',
            advisement: { description: '各教般分清次党名元点位保严设。' },
          },
          {
            name: '叶勇',
            server: '还做界平支则了系象众由划适号增这。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '带少话界着率第题节合指种声很得。',
            description: '布性第电史安高自省或来切化。',
            advisement: { description: '持点米以研须去或毛立林领先。' },
          },
          {
            name: '易霞',
            server: '型行着经感易话化意复认如己证自感组。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: true,
            code: '王代加技况多但条办织书头花后开党。',
            description: '长实儿你须准感装感达期声半。',
            advisement: { description: '住部些在么效为就量政参连阶。' },
          },
          {
            name: '常刚',
            server: '它把政命门民油厂等多定线元除商。',
            status: { '0': 'P', '1': 'E', '2': 'N', '3': 'D', '4': 'I', '5': 'N', '6': 'G' },
            result: { '0': 'P', '1': 'A', '2': 'S', '3': 'S', '4': 'E', '5': 'D' },
            recoverable: false,
            code: '实音阶他步活着可日相连现府。',
            description: '步军制西华很素打平格确收其速阶号线。',
            advisement: { description: '走引阶文称需料统说容全基同提共类真。' },
          },
        ],
      },
      msg: '回美等论区据值历们正应感准。',
      success: false,
    });
  },
};
