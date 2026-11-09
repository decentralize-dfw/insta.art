import json,csv,html,re,collections
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'instagram-review'/'publication-plan-180';OUT.mkdir(exist_ok=True)
CAP=OUT/'captions';CAP.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
assets={a['id']:a for a in read(ROOT/'archive-audit/audit-files.json')}
catalog={w['id']:w for w in read(ROOT/'yigit-site-repo/v3/content/works.json')}
base=read(ROOT/'instagram-review/working/plan-gun-1-90.json')
works={}
def work(key,slug,master,details,process=None):
 c=catalog[slug];works[key]={'key':key,'title':c['title'],'year':c['year'],'medium':c['medium'],'height_cm':c['height_cm'],'width_cm':c['width_cm'],'master':master,'details':details,'process':process or [],'metadata_source':'yigit-site-repo/v3/content/works.json','metadata_status':'local_catalogue_record','slug':slug}
def ids(a,b):return [f'A{x:04}' for x in range(a,b+1)]
works['painstaking']={'key':'painstaking','title':'Painstaking','year':2026,'medium':'Acrylic on canvas','height_cm':40,'width_cm':30,'panel_count':3,'master':'A0025','details':['A0018','A0019','A0015','A0008','A0017'],'process':[],'panels_left_to_right':['A0028','A0029','A0027'],'metadata_source':'painstaking-publish-report.json','metadata_status':'local_publication_record','slug':'painstaking'}
work('stlop','s-t-lop','A0134',ids(95,102))
work('angora','angora-mergvs','A1378',ids(1408,1413),['A1554','A1555',*ids(1560,1567),'A1556','A1557','A1558','A1559'])
work('virgil','virgil-on-virtual-cage-final-final-finalv9','A0582',ids(498,507),ids(428,439))
work('gxd','gxd-is-afk-we-banned-it','A1209',[],ids(1314,1323))
work('wall','walls-of-perception','A0258',ids(224,227),ids(260,264))
work('gary','gary-grills-cooper','A0298',ids(288,296))
work('mandarin','articulo-attack-on-mandarin','A0160',ids(135,141),ids(211,218))
work('sept','sept-neuf','A0947',ids(1034,1045),ids(1113,1131))
work('board','7-fam-board-game','A0592',ids(706,714),ids(664,676))
work('baby','baby-rights-101','A1809',ids(1795,1808))
work('capricorn','caprocorn-sister-war-plague-earthquake','A1832',ids(1811,1829))
work('cellular','cellular-spleens','A1862',ids(1844,1860))
work('ciao','ciao-capo-sono-squalo','A1903',ids(1874,1902))
work('duality','duality-of-the-angelic-summarization','A1945',ids(1928,1942))
work('good','good-people-helping-bad-ones-thats-why-theyre-bad-too','A2014',ids(2004,2013))
work('guard','guarding-holy-mountains-from-malice','A2050',ids(2025,2034))
work('materialize','how-to-materialize-your-loneliness-by-using-an-animal-in-somewhere-concrete-or-technologic','A2063',ids(2051,2062))
work('peachy','victim-psycho-logique-ii-the-peachy-pharaoh-connects-with-the-chair','A2156',ids(2135,2148))
work('morbid','morbid-forebodings-triggered-by-childish-landscape','A2182',ids(2175,2181))
work('transhumanism','century-of-0-1-transhumanism','A2213',ids(2191,2197))
work('unemployed','cute-but-unemployed-cartoon-figure','A2388',ids(2375,2387))
work('wings','wings-of-abyss','A2451',ids(2427,2437))
work('rompi','il-sbagliato-di-rompipalle','A1750',ids(1728,1746))
work('penguin','penguin-is-not-a-friend-only-a-sinner','A2743',['A2744','A2745','A2746'],ids(2740,2743))
work('viperella','viperella','A1772',ids(1762,1771))
work('greatfire','when-the-darkness-surrounds-be-among-those-who-burn-the-great-fire','A2423',ids(2403,2421))

music={
 'M1':{'title':'Signal to Noise','artist':'Scott Buckley','url':'https://www.scottbuckley.com.au/library/signal-to-noise/','start_seconds':30,'reason':'Yüzlerdeki huzursuzluğu destekleyen düşük yoğunluklu çello/piyano dokusu.'},
 'M2':{'title':'Hiraeth','artist':'Scott Buckley','url':'https://www.scottbuckley.com.au/library/hiraeth/','start_seconds':35,'reason':'Mekân ve bellek bölümlerinde sakin bir ses devamlılığı.'},
 'M3':{'title':'Undertow','artist':'Scott Buckley','url':'https://www.scottbuckley.com.au/library/undertow/','start_seconds':25,'reason':'Sahne ve figür ilişkilerinde ağır, düzenli bir eşlik.'},
 'M4':{'title':'Cirrus','artist':'Scott Buckley','url':'https://www.scottbuckley.com.au/library/cirrus/','start_seconds':40,'reason':'Yüzey ve geniş mekân okumalarında hafif atmosfer.'},
 'M5':{'title':'Filaments','artist':'Scott Buckley','url':'https://www.scottbuckley.com.au/library/filaments/','start_seconds':30,'reason':'Tarihli arşiv karşılaştırmalarında ölçülü piyano eşliği.'},
 'M0':{'title':'No music','artist':None,'url':None,'start_seconds':0,'reason':'Sessiz eser sunumu; fotoğraf ve carousel için bilinçli seçim.'}}
for m in music.values():
 if m['url']:m.update(license='CC BY 4.0',license_url='https://creativecommons.org/licenses/by/4.0/',verified_date='2026-10-28',excerpt_status='planned_edit_window_not_auditioned_or_beat_verified',delivery='Official MP3 → kurguya gömülü ses; Instagram müzik kataloğunda bulunması varsayılmaz.')

# Her haftanın beş ayrı editoryal işi; metinler yayın dili olan İngilizce.
weekly=[]
def week(a,b,theme,m,hook,decision,bridge,captions,carousel):
 weekly.append({'week':len(weekly)+1,'primary':a,'related':b,'theme':theme,'music_id':m,'hook':hook,'decision':decision,'bridge':bridge,'captions':captions,'carousel_points':carousel})
week('painstaking','stlop','Yüzü tanınır tutan ve bozan parçalar','M1','Three faces. Where does each one hold together?','The gap changes the face.','A face can stay readable without a stable outline.',[
 'An eye, a mouth, a familiar face. Then the brushwork pulls each feature in a different direction. Painstaking holds recognition and distortion in the same three-panel arrangement.',
 'Three panels, three different pressures on a face. Follow the eyes first, then the mouths, then the spaces between the canvases. The detail changes when it returns to the whole.',
 'The empty strip between two canvases is part of the viewing experience. Across that break, the eye starts comparing one face with another.',
 'Painstaking, presented as a complete triptych. The panel order matters: a close view gives one face; the full arrangement gives three faces in relation.',
 'In s(t)lop, the face is carried by colour and overlapping marks. Recognition survives even when the contour stops behaving like a clean boundary.'
],['Three faces. One arrangement.','Start with the eyes.','Now follow the mouths.','The gap changes the comparison.','Return to the complete triptych.'])
week('angora','virgil','Mekân figürden önce okunabilir mi?','M2','The figure is loud. The house holds the scene.','The same house, a different colour structure.','A room can do more than contain its figures.',[
 'The winged figure catches the eye. The house decides where that eye travels next: roof, doorway, window, back to the figure. Angora Mergvs gives the architecture an active role in the scene.',
 'Read Angora Mergvs from the building outward. The roof divides the image, the openings interrupt the blue, and the figure arrives inside that structure rather than outside it.',
 'These are recorded painting stages, aligned to the same frame. The building remains recognisable while its colour relationships change around the figure.',
 'Angora Mergvs in full. The house is more than a backdrop: its rooflines and openings carry the movement through the painting.',
 'In Virgil on Virtual Cage, the room closes around the group. Follow the ceiling edge, the hanging chair and the black-and-pink walls before returning to the figures.'
],['Read the house first.','The roof divides the image.','The openings interrupt the blue.','The figure sits inside this structure.','Return to the whole painting.'])
week('virgil','gxd','Tanıdık bir düzenin farklı sahneye dönüşmesi','M3','A familiar grouping, an unfamiliar room.','Follow the hands before the faces.','What holds a group together?',[
 'The grouping may look familiar, but the room changes its balance. In Virgil on Virtual Cage, hands, bodies and a hanging chair compete with the enclosing walls.',
 'A group can be read through its intervals. Follow the space between the figures, the direction of the hands and the edge of the room.',
 'A hand leads into another body; a dark boundary interrupts the route. This close view follows one connection through the group rather than explaining every reference at once.',
 'Virgil on Virtual Cage, complete. The ceiling remains visible because it changes how the group occupies the image.',
 'Gxd is AFK, We banned it also organises bodies as a group. The useful comparison is how their weight and spacing hold the scene together.'
],['A group inside a room.','Follow one hand.','Find the interval between bodies.','Follow the ceiling edge.','The group and room work together.'])
week('gary','unemployed','Kütle ve çizgiyle kurulan beden','M3','This body is built from colour masses.','The silhouette carries the weight.','A familiar figure can become an unstable body.',[
 'The orange field makes the body immediately readable. Inside that outline, purple and green pull its volume in different directions.',
 'Look at the silhouette first, then the colour inside it. The figure holds its weight through the relationship between the two.',
 'One edge is enough to change the body. This close view follows the boundary where the figure meets the orange ground.',
 'gary grills cooper, complete. The empty orange around the figure is part of how its weight becomes visible.',
 'The rounded figure in cute but unemployed cartoon figure is held against a red field. Compare its outer edge with the divided body in gary grills cooper.'
],['Start with the silhouette.','Locate the purple mass.','Follow the green interruption.','Compare edge and ground.','Return to the complete figure.'])
week('wall','angora','Geometrik mekân ve yumuşak figür','M2','A hard edge beside a soft body.','The table changes the reading of the figure.','Two spaces, two ways of directing the eye.',[
 'A red table and a green field set up firm divisions. The figure crosses those divisions with a much less stable outline.',
 'Put the room edge beside the figure edge. One organises the space; the other keeps the body open to change.',
 'The red table gives the eye a place to land. From there, the yellow passage carries it back into the figure.',
 'walls of perception, complete. Its hard divisions and loose figure need to be seen together.',
 'In Angora Mergvs, rooflines take on the organising role that the table plays in walls of perception. Similar attention, different architecture.'
],['Hard edge / soft edge.','The table gives a horizontal.','The body interrupts it.','Compare the two boundaries.','See both in the whole.'])
week('board','sept','Sahneye iki farklı bakış','M3','The pieces are figures too.','Look at what sits between the players.','A small figure can redirect the whole scene.',[
 'Two larger figures face one another, but the smaller figures on the board complicate the encounter. The centre is occupied, not empty.',
 'Read the two sides separately, then look at what happens between them. The board creates a second scale of bodies within the painting.',
 'The small pieces change the scale of the scene. This close view stays with them before returning to the two larger figures.',
 '7 fam board game, complete. The centre matters as much as either face.',
 'In sept neuf, the bird beside the seated figure creates another point of attention. A secondary figure can change where the scene seems to look.'
],['Two sides of one scene.','Read the left figure.','Read the right figure.','The centre has bodies too.','Return to both scales together.'])
week('painstaking','stlop','Yüzeye bakmak için ses gerekli mi?','M1','Let the painted eye stay on screen.','Look at the marks without a soundtrack.','Another face, the same time to look.',[
 'A painted eye is also a patch of colour and a set of marks. This close view leaves time for both readings.',
 'Recognition happens quickly; the surface takes longer. Move between a full panel and its eye detail without changing the colour treatment.',
 'No music on this version. The image stays with the painted eye and returns to the complete panel.',
 'Painstaking, complete. The detail is one way in; the three-panel arrangement remains the work.',
 's(t)lop offers another face in which colour and contour keep separating. The question is still what lets recognition survive.'
],['A face, then a surface.','One painted eye.','The marks around it.','The whole panel again.','The triptych restores the comparison.'])
week('baby','cellular','2020 arşivi: bedenin çoğalması','M5','Where does one body end?','A red line interrupts the black and white.','A body can multiply without becoming a crowd.',[
 'In baby rights 101, black-and-white bodies fold into one another. A thin red line offers a different route through the knot.',
 'Follow one contour until it stops belonging to a single body. These details return the close view to the complete 2020 painting.',
 'The red passage is small in area and large in effect. It interrupts the black-and-white structure without separating every figure.',
 'baby rights 101, from the 2020 archive. Shown as a complete painting, with its own date rather than as new production.',
 'cellular spleens turns the question outward: eyes and organic forms accumulate across a pale ground. Another 2020 solution to a body that will not stay singular.'
],['Where does one body end?','Follow a black contour.','Find the red interruption.','The same passage in the whole.','A complete painting from 2020.'])
week('penguin','angora','Figür ile çevresi arasında ölçek','M4','The whole changes the scale of the detail.','A detail cannot tell you the physical size.','A building gives the figure another scale.',[
 'The grey and yellow structure in penguin is not a friend, only a sinner can read as a face, a body or a field of paint. The full view keeps those readings in tension.',
 'A detail describes the surface; a documented photograph with the painting describes physical scale. They answer different questions.',
 'The square composition matters. Follow a curved passage, then return to all four edges before deciding what the form is doing.',
 'penguin is not a friend, only a sinner, 2023. The full square is preserved rather than cropped into a portrait-shaped image.',
 'The house in Angora Mergvs gives the winged figure a different scale. Compare that relation with the more ambiguous body and ground of the 2023 painting.'
],['Surface and scale are different.','A painted passage.','Its place in the square.','Documented physical scale.','Return to the complete painting.'])
week('capricorn','duality','Birden fazla bedeni aynı alanda tutmak','M5','Three bodies share a dark field.','Empty areas hold the figures apart.','Another way to divide a figure.',[
 'The dark field separates some passages and joins others. In caprocorn sister, the distance between the bodies is part of the composition.',
 'Read the spaces between the figures before their faces. Those intervals change how the group is held together.',
 'A pale opening can behave like part of a face or like a break in it. This close view follows that uncertainty back into the group.',
 'caprocorn sister: war, plague, earthquake, from 2020. Presented in its final dark-field state.',
 'duality of the angelic summarization offers a different division: the uncertainty sits within the figure as much as between bodies. Its archive date is 2019.'
],['Read the dark field.','Find the upper bodies.','Find the lower body.','Follow the intervals.','Compare them in the whole.'])
week('sept','board','İzleyici sorusu yoksa açık editoryal soru','M3','What changes when you notice the bird?','The eye and the bird do not share a scale.','The secondary figure can become the centre.',[
 'An editorial question for this painting: what changes when the bird becomes the first thing you notice? Follow its position beside the seated figure.',
 'The eye, the hand and the bird organise different routes through sept neuf. This sequence makes those routes visible without inventing an audience question.',
 'Stay with the pale eye, then widen the frame. A detail that seems isolated changes its role inside the seated body.',
 'sept neuf, complete. The surrounding green is kept visible because it separates the main figure from its smaller companion.',
 'The smaller bodies on the board in 7 fam board game can also take over the scene. Scale is not the same as compositional importance.'
],['An editorial question.','The seated figure.','The eye and hand.','The bird beside it.','Which route did you follow?'])
week('gxd','mandarin','Referansın ötesinde kendi kompozisyonu','M3','Read the group before naming the reference.','Bodies carry the scene.','Another scene held in suspension.',[
 'Begin with the bodies, their weight and the spaces between them. Gxd is AFK, We banned it can be examined before any reference is named.',
 'A reference is one part of the context. This sequence stays with the painting itself: grouping, direction and the intervals that hold the scene together.',
 'The simplest edit can still make a complete point. A full view, one connected passage, and a return to the group.',
 'Gxd is AFK, We banned it, complete. A quiet presentation of the painting after the closer readings.',
 'In articulo attack on mandarin, suspended and floating forms organise another kind of unstable scene. Compare their directions with the grouped bodies in Gxd.'
],['Begin with this painting.','Locate the group.','Follow a connected passage.','Read the surrounding interval.','Return to the full composition.'])
week('ciao','rompi','90. gün kontrolü: yüz ve siluet','M5','Two figures, two interrupted outlines.','A large hand changes the body beside it.','A face does not need a smooth contour.',[
 'Two long figures occupy the red-and-black field. Their outlines are interrupted, but their relation remains readable.',
 'A face, a hand and the gap between two figures give three different scales of information. This is an archive painting, not a new studio update.',
 'The hand takes up more visual room than its size alone suggests. Follow its edge back toward the body.',
 'ciao capo, sono squalo, 2020. Full view, with the complete relation between the two figures preserved.',
 'In il sbagliato di rompipalle, the face breaks into separate passages. This 2019 painting carries the recognition question in another direction.'
],['Two interrupted outlines.','A face close up.','A hand at another scale.','The gap between figures.','The complete 2020 painting.'])
week('cellular','morbid','Göz ve organik form arasında','M4','When does a cluster become a body?','The pale ground keeps the forms apart.','Another organic body, another ground.',[
 'Eyes and rounded forms accumulate across cellular spleens. The pale field gives the cluster enough space to stay readable.',
 'The same cluster can be followed through its eyes, edges or empty spaces. Each route changes what looks like a body.',
 'A close view can hide the pale ground that separates the forms. Widening the frame restores that separation.',
 'cellular spleens, 2020. The final painting is shown without the effect variants from the archive.',
 'morbid forebodings triggered by childish landscape bends an organic body through a different coloured field. It is the 2019 work, distinct from the square 2023 penguin painting.'
],['A cluster or a body?','Start with the eyes.','Follow an outer edge.','Notice the pale intervals.','Restore the whole cluster.'])
week('guard','peachy','Asılı beden ve oda sınırları','M3','The body hangs against a divided room.','A straight boundary makes the bend visible.','Another body suspended beside a chair.',[
 'The room divides into strong blocks of colour. Against them, the suspended body becomes harder to read as a stable upright figure.',
 'Follow a straight room edge, then the body beside it. The comparison makes the bend visible.',
 'The surrounding blocks give the suspended form its direction. This close view keeps an edge of the room in frame.',
 'guarding holy mountains from malice, 2019. The complete room is retained around its figures.',
 'In the peachy pharaoh painting, an elongated body and a drawn chair offer another suspended relation. Compare the two compositions without turning them into the same story.'
],['A divided room.','One straight boundary.','The body against it.','Another figure in the field.','Return to the complete room.'])
week('materialize','good','Birbirine bağlanan ve ayrılan figürler','M4','Two sides share a crowded surface.','Follow the passage that joins them.','A group can be read through its gaps.',[
 'A face at one side and a smiling head at the other pull attention across the surface. The marks between them do the connecting work.',
 'Instead of isolating every figure, follow one route across the image. See where paint joins forms and where the ground opens between them.',
 'One connected passage can carry the eye across an otherwise crowded composition. The full view shows where that route ends.',
 'How to materialize your loneliness by using an animal in somewhere concrete or technologic, 2019. Presented as a complete painting.',
 'In good people helping bad ones, larger pale forms and smaller orange figures create another group relation. Look at their intervals before reading the title as a story.'
],['Follow one route.','Start at the left face.','Cross the connecting marks.','Find the right-hand head.','Return to the whole route.'])
week('wings','angora','Kanatlı figürün iki farklı mekânı','M2','A wing changes the direction of a body.','Follow the spiral, not only the face.','The same motif does a different job.',[
 'The pale pointed head and the spiral below it pull in different directions. The surrounding dark field gives both a strong edge.',
 'A winged form can be examined through its head, spiral and relation to the smaller suspended figure. These are different parts of one composition.',
 'The spiral carries movement beyond the head. Keep its turn visible before returning to the whole painting.',
 'wings of abyss, 2019. A complete archive painting, shown in its own colour structure.',
 'Angora Mergvs also contains a winged figure, but architecture gives it another setting. A shared motif does not make the two paintings the same scene.'
],['A winged form.','The pale pointed head.','The spiral below it.','The smaller suspended figure.','All directions in one frame.'])
week('viperella','painstaking','Uzun beden ve parçalanmış yüz','M1','An elongated body, a small change of edge.','The raised hand changes the silhouette.','From one extended figure to three faces.',[
 'The long figure in viperella is interrupted by the raised hand and the red mouth. Small passages change how the whole body is read.',
 'Look at the head, hand and outer contour in turn. Their spacing is easier to understand when the full figure returns.',
 'The raised hand interrupts a long vertical route through the image. Keep the surrounding ground visible to see the break.',
 'viperella, 2020. The final archive master is used here rather than the older, differently lit phone photograph.',
 'Painstaking compresses the face into three adjacent panels. Compare that concentrated arrangement with the extended body in viperella.'
],['An extended figure.','The mouth.','The raised hand.','The interrupted contour.','The whole body again.'])
week('greatfire','duality','Koyu alanın figürü taşıması','M5','The dark field gives the head its edge.','A raised hand changes the route upward.','A different face against a different darkness.',[
 'The head and raised hand stand against a dark green field. Their separation from that ground gives the figure its first reading.',
 'The full view keeps the dark areas active. They are not leftover space around the coloured body.',
 'Follow the hand toward the head, then widen the frame. The route depends on what the dark ground leaves visible.',
 'When the Darkness surrounds, be among those who burn the Great Fire, 2020. The full composition follows the title recorded in the catalogue.',
 'duality of the angelic summarization uses another dark colour relation around a divided figure. The two works share a question, not a single interpretation.'
],['The dark field is active.','Locate the head.','Follow the raised hand.','Read the space around both.','Return to the complete figure.'])
week('transhumanism','gxd','Mekanik merkez ve çevresindeki bedenler','M3','A dark centre divides the bodies.','Read the object and figures together.','A group does not need a single centre.',[
 'The dark mechanical form occupies the centre while coloured bodies sit around it. The relation between them carries the composition.',
 'The centre, the two sides and the painted writing give different kinds of information. This sequence separates them, then restores the whole.',
 'Isolating the centre loses the bodies that give it scale. The close view keeps their boundary in frame.',
 'Century of 0 & 1 / Transhumanism, 2019. The writing and signs remain visible as parts of the painting.',
 'In Gxd is AFK, We banned it, weight is distributed through a group of bodies. Compare that with the concentrated dark centre in Transhumanism.'
],['A dark centre.','The body on one side.','The body on the other.','Writing within the painting.','The full relation returns.'])
week('mandarin','wall','Akışın resim boyunca yön değiştirmesi','M4','A floating form sends the eye across the canvas.','The blue passage joins distant parts.','A colour passage can organise another scene.',[
 'Blue forms cross the dark field while the boat and figures hold another scale below. The painting gives the eye more than one direction.',
 'Follow the suspended figure, the pale mountain and the boat as separate anchors. The full view shows how they share the same field.',
 'The blue passage does not stop at one object. This close view follows its direction back into the complete square.',
 'articulo attack on mandarin, 2026. The square composition is preserved in full.',
 'The yellow passage in walls of perception offers another route through a figure and its setting. Compare direction rather than colour alone.'
],['One field, several anchors.','A suspended figure.','The pale mountain.','The boat below.','Follow the blue between them.'])
week('penguin','baby','Yakın planın kaybettirdiği bilgi','M4','A close view can hide the painting.', 'Restore the edge of the canvas.','Two different ways to lose the body.',[
 'This time the close view comes first. The full square restores information that the surface detail could not provide.',
 'A crop is a viewing choice, not a second painting. Compare the same passage with and without the four edges of the composition.',
 'The outer edge locates the curved form. The edit widens the view instead of manufacturing a transformation.',
 'penguin is not a friend, only a sinner, 2023. Full view after the close readings.',
 'In baby rights 101, a close view can also make it difficult to separate bodies. The cause is different: interlocking contours rather than the square field of the 2023 painting.'
],['A detail comes first.','What has the crop hidden?','Locate it in the square.','Restore all four edges.','One painting, two viewing distances.'])
week('sept','capricorn','Grupta ve tek figürde boşluk','M3','The green around the figure is doing work.','A small companion changes the interval.','Empty space works differently around a group.',[
 'The seated figure does not occupy all the green. That surrounding interval helps separate it from the bird beside it.',
 'Follow the figure, the bird and the space between them. The empty-looking passage is part of their relation.',
 'The bird changes the distance the eye has to cross. This edit stays with that interval rather than adding another reference.',
 'sept neuf, 2026. The surrounding field is preserved in the full view.',
 'In caprocorn sister, dark intervals separate several bodies. Compare that group structure with the smaller companion beside the seated figure in sept neuf.'
],['Read the surrounding green.','The seated figure.','The smaller companion.','The interval between them.','The whole scene again.'])
week('gary','ciao','Siluetten detaya giden iki yol','M3','Can the silhouette carry the first reading?','A small mark changes a large mass.','Two figures need another kind of boundary.',[
 'Read the figure as a silhouette before looking inside it. The orange ground makes that first route possible.',
 'Silhouette, internal mass, small facial passage: three viewing distances give three different kinds of information.',
 'A small mark can redirect attention across a much larger body. The edit makes the connection visible before returning to the silhouette.',
 'gary grills cooper, 2026. Full view after the separate readings of edge and internal colour.',
 'The two figures in ciao capo, sono squalo share a field rather than a single silhouette. Compare how their gap takes on the boundary work.'
],['Begin with the silhouette.','Read the internal mass.','Find the small facial passage.','Place it back in the body.','Return to the full edge.'])
week('painstaking','angora','İki ana sorunun tekrar okunması','M1','A face holds together. A space holds a scene.','Which relation survives the close view?','Different subjects, a related way of looking.',[
 'Return to Painstaking with the whole arrangement first. Recognition is held across features, brushwork and the breaks between panels.',
 'The same source can answer a new question. This sequence compares an eye detail with the panel interval rather than repeating the opening-week edit.',
 'The close view is useful only if its role in the whole becomes clear. Follow one painted eye back to its panel and then to the triptych.',
 'Painstaking, complete. The three panels remain in the same left-to-right order used at the start of this plan.',
 'Angora Mergvs moves from facial recognition to spatial orientation. Both ask the viewer to hold a local passage and a larger arrangement together.'
],['Return to the arrangement.','A painted eye.','Its place in one panel.','The interval beside that panel.','Three panels in the same order.'])
week('gxd','wings','180. gün kapanışı ve sonraki dönemin sorusu','M3','What remains clear without naming a reference?','A group, a connection, a complete view.','A shared question can continue in another painting.',[
 'A group of bodies, the spaces between them and the weight they carry: the painting offers a complete point of entry before its references are named.',
 'This closing selection keeps one question in view: how do bodies and their surroundings hold a scene together? The images provide the evidence.',
 'One connected passage, shown at two distances. The return to the whole is the point of the edit.',
 'Gxd is AFK, We banned it, complete. The next selection can begin with another painting and the same attention to how its scene holds together.',
 'wings of abyss would continue the question through a different body and field. This is a reserve idea beyond Day 180, not an extra closing-day post.'
],['A group before a reference.','A connected passage.','The surrounding interval.','The complete painting.','One question for the next selection.'])

def credit(w):
 if w.get('panel_count'):return f"{w['title']}\n{w['year']} · {w['medium']}\nTriptych · 3 panels, each {w['height_cm']} × {w['width_cm']} cm (h × w)."
 return f"{w['title']}\n{w['year']} · {w['medium']}\n{w['height_cm']} × {w['width_cm']} cm (h × w)."
def audio_credit(m):
 if not m['url']:return ''
 return f"Music: {m['title']} — Scott Buckley. CC BY 4.0. Excerpt; volume adjusted.\n{m['url']}\nhttps://creativecommons.org/licenses/by/4.0/"
def detail(w,n):return w['details'][n%len(w['details'])] if w['details'] else w['master']
posts=[];days=[]
for n in range(1,181):
 wi=(n-1)//7;cy=(n-1)%7+1;w=weekly[wi];A=works[w['primary']];B=works[w['related']]
 d={'day':n,'week':wi+1,'cycle_day':cy,'timezone':'Europe/Paris','status':'planned_not_published','actual_published_at':None,'ad_budget_eur':0,'theme':w['theme'],'is_feed_post':cy in [1,2,4,5,6]}
 if not d['is_feed_post']:
  d.update(time='18:00',task=('Sonraki haftanın beş dosyasını hazırla; künye, renk, metin, ses ve kaynak eşlemesini kontrol et.' if cy==3 else 'Aynı yaştaki gönderileri değerlendir; gerçek sonuç ve üretim süresini kaydet. Tek sonraki değişikliği seç.'),story='Zorunlu Story yok. Yalnız gerçek geri bildirim varsa İngilizce özet.')
  days.append(d);continue
 ix={1:0,2:1,4:2,5:3,6:4}[cy];workobj=B if cy==6 else A
 fmt={1:'Reel R1',2:'Carousel C1',4:'Reel R2',5:'Single P1',6:'Reel R3'}[cy]
 duration=24 if 'Reel' in fmt else 0
 mid=w['music_id'] if duration else 'M0'
 if wi==6 and cy==4:mid='M0'
 mus=music[mid];caption=w['captions'][ix]+'\n\n'+credit(workobj)
 if duration and audio_credit(mus):caption+='\n\n'+audio_credit(mus)
 aid=[workobj['master'],detail(workobj,0),detail(workobj,1)] if duration else ([A['master'],detail(A,0),detail(A,1),detail(A,2),A['master']] if cy==2 else [A['master']])
 if cy==6:aid=[A['master'],B['master'],detail(B,0),detail(B,1)]
 title=[w['hook'],w['carousel_points'][0],w['decision'],workobj['title'],w['bridge']][ix]
 p={'id':f'P{len(posts)+1:03}','day':n,'week':wi+1,'cycle_day':cy,'time':'19:00','timezone':'Europe/Paris','format':fmt,'status':'detailed_editorial_plan_not_rendered' if n<=14 else 'draft_revalidate_weekly','title_en':title,'work_keys':[A['key'],B['key']] if cy==6 else [A['key']],'primary_work_key':workobj['key'],'asset_ids':list(dict.fromkeys(aid)),'duration_seconds':duration,'music_id':mid,'music_window_seconds':[mus['start_seconds'],mus['start_seconds']+duration] if duration and mid!='M0' else None,'music_mix':'Müzik yaklaşık −24 LUFS integrated, true peak ≤ −3 dBTP; 0,3 sn giriş / 0,8 sn çıkış. Editör başlangıç hedefi, Instagram şartı değil.' if mid!='M0' else 'Müzik ekleme. Arşiv videolarındaki arka plan müziğini de kullanma.','caption_en':caption,'alt_text_en':f"{workobj['title']}, {workobj['year']}, by Yiğit Özen. "+assets[workobj['master']].get('visual_note',''),'story_time':'19:20','story_text_en':title,'story_asset_id':detail(workobj,0),'story_action':'Tek kare ayrıntı + ilgili gönderi paylaşımı; müzik yok. Soru varsa gerçek cevapları daha sonra değerlendir.','measurement_hours':[24,72,168],'primary_metric':('saves_and_work_specific_questions' if cy==2 else 'work_specific_questions_and_profile_visits' if cy==4 else 'likes_per_reach_and_work_inquiries' if cy==5 else 'attributed_follows_where_available_and_shares'),'ad_status':'organic_only_no_activation_assigned','caption_file':f"captions/GUN-{n:03}_{fmt.split()[0].upper()}.txt",'editorial_language':'en','rendered_media_path':None,'prepublish_checks':['Kaynak görüntü ve renk tutarlılığı','Künye kaynağı ve panel sırası','Mobil metin okunurluğu','Ses/kredi ve dosya önizlemesi','Stok/fiyat/temsil iddiası eklenmedi']}
 if duration:
  if cy==1:p['edit_tr']='0–3 sn bütün ve kapak sorusu; 3–9 sn ilk detay; 9–16 sn ikinci detay; 16–24 sn bütüne dönüş ve tek sonuç. Hafif kamera hareketi; renk efekti yok.'
  elif cy==4:p['edit_tr']='0–3 sn tek karar cümlesi; 3–10 sn gerçek detay; 10–17 sn detayın yakın çevresi; 17–24 sn bütün. Detayları aynı resmin incelemesi olarak göster; olmayan süreç üretme.'
  else:p['edit_tr']='0–4 sn ilk eserdeki ortak soruyu bütünle kur; 4–9 sn ikinci eser bütünü; 9–17 sn ikinci eserde iki detay; 17–24 sn ikinci bütün ve önemli fark. Yıllar ekranda; seri bilgisini bilmeyen kişi de anlayabilsin.'
 elif cy==2:p['edit_tr']='5 sayfa: soru/kapak → ilk görsel kanıt → ikinci kanıt → iki kanıtın ilişkisi → künyeli bütün. Her sayfa farklı iş yapar; tamamlanmış eseri süreç gibi sunma.';p['slide_texts_en']=w['carousel_points']
 else:p['edit_tr']='Tam eser, orijinal oranı korunarak nötr paspartu içinde. Kırpma, efekt, yapay galeri mockup veya görüntüyü örten metin yok. Caption künye ve tek bağlam taşır.'
 posts.append(p);d.update(time='19:00',post_id=p['id'],format=fmt,task=p['title_en'],story='19:20 · '+p['story_text_en']);days.append(d)

# Deneyler orijinal Ayak 4 sırasını korur; 90 gün sonrası yeni tasarım kararlarıdır.
for w in weekly:
 wi=w['week'];w.update(day_range=[(wi-1)*7+1,min(wi*7,180)],status='planned',review='Gün 3/7 üretim ve değerlendirme; yayınlar 24/72/168 saatte gerçek yaşlarıyla karşılaştırılır.')
 if wi<=13:w['learning_question']=base['weeks'][wi-1]['test'];w['controls']=base['weeks'][wi-1]['keep']
 else:
  w['learning_question']='İlk 90 günde anlaşılır bulunan anlatım ilkesini bu esere aktar; yeni ses/saat/format değişkenini aynı anda açma.'
  w['controls']='Saat 19.00, ana dil İngilizce, haftalık hacim sabit. Sonuca göre tek geri alınabilir değişiklik.'
 if wi==2:w['learning_question']='D08 sonuç-önce, D13 mekân sorusu-önce. İki farklı eser olduğundan yalnız yön gösteren eşleştirme; temiz A/B veya giriş sırası üstünlüğü sonucu çıkarma.'
 if wi==7:w['learning_question']='Müzikli D43 ve sessiz D46 aynı eserin farklı detaylarını kullanır; ses etkisi için keşif gözlemi. Temiz karşılaştırma istenirse aynı kurgu iki yerel önizlemede hazırlanır, yeniden yükleme zorunlu değil.'

# İlk iki haftanın gerçek dosyalarla saniyeli ve sayfalı üretim kartları.
def P(day):return next(p for p in posts if p['day']==day)
def shot(start,end,asset,text,action):return {'start':start,'end':end,'asset_id':asset,'on_screen_en':text,'edit_tr':action}
P(1)['shots']=[shot(0,3,'A0025','Three faces. What keeps them readable?','Bütün triptiği 9:16 alanına sığdır; panel sırası solda A0028, ortada A0029, sağda A0027.'),shot(3,8,'A0018','Start with the eyes.','Sağ panelde iki göz; mevcut detayın %100–105 yavaş ölçeklenmesi.'),shot(8,13,'A0019','An eye can also be a field of paint.','Orta panelin iri göz detayı; renk ayarı öncekiyle aynı.'),shot(13,18,'A0015','Recognition survives the broken contour.','İki panelin sınırı ve yüz parçaları; panel aralığını kesme.'),shot(18,24,'A0025','Painstaking · 2026\nThree panels, one arrangement.','Bütüne dön; son 3 saniye sabit. Başlık son kartta küçük.')]
P(1)['caption_en']="A face becomes readable before every feature makes sense. In Painstaking, the eyes, mouths and painted edges keep pulling in different directions.\n\nThe close views belong to the same triptych. Returning to all three panels changes how each face is read.\n\n"+credit(works['painstaking'])+'\n\n'+audio_credit(music['M1'])
P(1)['cover_en']='THREE FACES\nONE ARRANGEMENT';P(1)['story_text_en']='Which did you notice first: an eye, a mouth, or the space between panels?';P(1)['story_action']='A0018 ayrıntısı, İngilizce soru etiketi; gerçek cevap gelmezse sonuç üretme.'
P(2)['slides']=[{'page':1,'asset_id':'A0025','text_en':'Three faces.\nOne arrangement.','layout_tr':'Bütün triptik ortada; üstte kısa başlık. Panel sırası korunur.'},{'page':2,'asset_id':'A0018','text_en':'Start with the eyes.\nTwo eyes, two different pressures.','layout_tr':'Hazır detayın çevresini koru; metin nötr alt bantta.'},{'page':3,'asset_id':'A0015','text_en':'Now follow the mouths.\nThe contour will not stay still.','layout_tr':'Aynı detay kadrajını esnetme; yüzeyin üzerine metin bindirme.'},{'page':4,'asset_id':'A0008','text_en':'The gap changes the comparison.\nThe panels remain separate.','layout_tr':'İki panel arasındaki gerçek boşluk görünür; dijital kesme gibi sunma.'},{'page':5,'asset_id':'A0025','text_en':'Return to the complete triptych.\nPainstaking · 2026\nAcrylic on canvas\n3 panels, each 40 × 30 cm','layout_tr':'Tam triptik; künye altta. Ölçü yüksekliğe × genişliğe göre.'}]
P(2)['caption_en']='Three ways to begin looking at the same triptych: the eyes, the mouths, and the breaks between panels.\n\nEach close view gives different information. The last slide restores the arrangement that connects them.\n\n'+credit(works['painstaking'])
P(2)['story_text_en']='The detail changes when it returns to the whole.'
P(4)['shots']=[shot(0,4,'A0008','The gap changes the face.','Hazır iki panel detayında boşluğu göster; yeni çizgi veya morf efekti ekleme.'),shot(4,10,'A0029','One panel: a face.','Orta panel bütünü; baş ve ağız aynı anda görünür.'),shot(10,16,'A0008','Beside another: a comparison.','Aynı boşluğa geri dön; sabit kadraj.'),shot(16,24,'A0025','Three separate panels.\nOne viewing arrangement.','Bütün düzeni göster; izleyiciye karşılaştırma için süre ver.')]
P(4)['caption_en']='A strip of empty space separates the canvases. It also gives the eye a place to stop and compare.\n\nThis is a close reading of the finished triptych, not a record of its painting process. The three canvases remain separate; the arrangement brings their faces into relation.\n\n'+credit(works['painstaking'])+'\n\n'+audio_credit(music['M1'])
P(4)['story_text_en']='One panel gives a face. The arrangement gives a comparison.'
P(5)['caption_en']='Painstaking, in full.\n\nThree faces share a restrained ground while their features pull in different directions. The panel breaks remain visible because they are part of how the work is encountered.\n\n'+credit(works['painstaking'])
P(5)['story_text_en']='Painstaking · 2026\n3 panels, each 40 × 30 cm';P(5)['story_asset_id']='A0025'
P(6)['shots']=[shot(0,4,'A0134','A face without a stable outline.','STLOP bütününü ilk karede göster; başka videonun devamı bilgisi gerekmesin.'),shot(4,10,'A0096','Colour keeps the face readable.','Göz, burun ve çevre boyası; %100–105 hareket.'),shot(10,17,'A0097','The marks cross its contour.','Alt yüz ve çevre; ağır geçiş.'),shot(17,24,'A0134','s(t)lop · 2026\nThe whole keeps both readings.','Bütüne dön; künye sade ve küçük.')]
P(6)['caption_en']='The face in s(t)lop is carried by overlapping colour as much as by its outline. A close view can become an arrangement of marks; the full painting makes the figure readable again.\n\nA different solution to the question of what keeps a face recognisable.\n\n'+credit(works['stlop'])+'\n\n'+audio_credit(music['M1'])
P(6)['work_keys']=['stlop'];P(6)['story_text_en']='Where does the face stop and the surrounding paint begin?'
P(8)['shots']=[shot(0,3,'A1378','The figure is loud.\nThe house holds the scene.','Bütün ilk kare; başlık üst nötr alanda.'),shot(3,9,'A1410','The roof divides the image.','Çatı ve pencere; telefon/kamera kenarını göstermeden resim alanına kırp.'),shot(9,15,'A1409','Openings pull the eye through it.','Kapı, merdiven ve mavi cephe; tuval dışındaki ahşabı kırp.'),shot(15,19,'A1413','The figure arrives inside that structure.','Üst kanatlı figür; tuval kenarı dışını kırp.'),shot(19,24,'A1378','Angora Mergvs · 2026\nRead the house again.','Bütüne dön; aynı renk görünümü.')]
P(8)['caption_en']='The winged figure catches the eye. The house decides where that eye travels next.\n\nRooflines divide the image; doors and windows interrupt the blue. Looking at the architecture first changes the place of the figure within the scene.\n\n'+credit(works['angora'])+'\n\n'+audio_credit(music['M2'])
P(8)['story_text_en']='Read the house before the figure.';P(8)['story_asset_id']='A1410'
P(9)['slides']=[{'page':1,'asset_id':'A1378','text_en':'Read the house first.','layout_tr':'Bütün resim; başlık resim dışında.'},{'page':2,'asset_id':'A1410','text_en':'The roof divides the image.','layout_tr':'Çatı çizgilerini koru; çekim çevresindeki ahşabı çıkar.'},{'page':3,'asset_id':'A1409','text_en':'The openings interrupt the blue.','layout_tr':'Kapı ve merdiven detayı; sağdaki ahşap kenarı kırp.'},{'page':4,'asset_id':'A1413','text_en':'The figure sits inside this structure.','layout_tr':'Kanat ve gövdeyi birlikte tut; üstteki tuval dışını çıkar.'},{'page':5,'asset_id':'A1378','text_en':'Angora Mergvs · 2026\nAcrylic on canvas\n120 × 100 cm','layout_tr':'Tam eser ve künye; ölçü yüksekliğe × genişliğe göre.'}]
P(9)['caption_en']='Roof, opening, figure, whole.\n\nThis sequence reads Angora Mergvs through its architecture. The building is not neutral space behind the character: its edges and openings organise the route through the painting.\n\n'+credit(works['angora'])
P(9)['story_text_en']='Roof → opening → figure → whole.';P(9)['story_asset_id']='A1409'
P(11)['shots']=[shot(0,3,'A1559','The same house.\nA different colour structure.','Bitmiş son kayıtla aç; doğru renk, remiks değil.'),shot(3,6,'A1554','Recorded painting stages','FRAMED/0 çizgi başlangıcı, fiziksel süreç dizisinin başı.'),shot(6,9,'A1560','Early colour blocks','FRAMED/2: sarı ev, kırmızı çatı. Efektli önce/sonra değil.'),shot(9,12,'A1564','The structure stays readable.','FRAMED/6: koyu ev ve pembe çevre.'),shot(12,15,'A1556','Colour changes the relation.','FRAMED/10: mavi bina, koyu çatı.'),shot(15,18,'A1557','The figure changes with it.','FRAMED/12: figürün gelişimi.'),shot(18,24,'A1559','Angora Mergvs · 2026\nActual stages, aligned to one frame.','FRAMED/14: son süreç karesi; fotoğraf geçişi olduğunu açık bırak.')]
P(11)['caption_en']='The building remains recognisable while its colour relationships change around the figure.\n\nThese are photographs of recorded painting stages, already aligned to the same frame. The changes belong to the painting process; they are not a digital colour effect applied to the final image.\n\n'+credit(works['angora'])+'\n\n'+audio_credit(music['M2'])
P(11)['story_text_en']='Recorded stages. Same frame. Different colour relationships.';P(11)['story_asset_id']='A1560'
P(12)['caption_en']='Angora Mergvs, in full.\n\nThe rooflines, doors and windows carry the eye through the blue architecture and back toward the figure. This full view follows the close readings and the recorded stages.\n\n'+credit(works['angora'])
P(12)['story_text_en']='Angora Mergvs · 2026\nAcrylic on canvas · 120 × 100 cm';P(12)['story_asset_id']='A1378'
P(13)['shots']=[shot(0,3,'A0504','Can a room hold a group in place?','Mekân detayıyla soru-önce aç; tavan ve çizgiler görünür.'),shot(3,9,'A0582','Follow the ceiling edge.','İlk geniş açılım; gerçek tavan çerçevesi.'),shot(9,15,'A0502','Then the hanging chair.','Sandalye detayı; düz çizgiler gerilim yaratıyor yorumunu metne yığma.'),shot(15,19,'A0506','The figures occupy that enclosure.','Grup detayı; sıcak bedenler.'),shot(19,24,'A0582','Virgil on Virtual Cage · 2026\nThe room is part of the grouping.','Bütün ve doğru kısa başlık; tam başlık captionda.')]
P(13)['caption_en']='The room does more than sit behind the figures. Its ceiling edge, dark walls and hanging chair help enclose the group.\n\nFollow those boundaries first, then return to the bodies. The scene changes when the surrounding space becomes part of the reading.\n\n'+credit(works['virgil'])+'\n\n'+audio_credit(music['M2'])
P(13)['work_keys']=['virgil'];P(13)['story_text_en']='Follow the ceiling edge before the faces.';P(13)['story_asset_id']='A0504'

first_alt={1:'Three adjacent painted faces in separate vertical canvases, with violet, pink, yellow and grey features against an olive ground.',2:'A five-slide view of the Painstaking triptych, moving from the full arrangement to eyes, mouths and the breaks between canvases.',4:'A close reading of the physical gap between adjacent panels of the Painstaking triptych.',5:'Painstaking, 2026: three separate vertical paintings of distorted faces, shown in left-to-right order.',6:'s(t)lop, 2026: a vertical painting with a loose face and figure in pale pink, yellow, violet and turquoise.',8:'Angora Mergvs, 2026: a blue house with dark rooflines and openings beneath an orange winged figure.',9:'Five slides move through the roof, openings, winged figure and complete view of Angora Mergvs.',11:'Aligned photographs show Angora Mergvs developing from a drawing and yellow buildings into blue architecture with an orange winged figure.',12:'Angora Mergvs, 2026, acrylic on canvas, 120 by 100 centimetres: blue architecture and an orange winged figure.',13:'Virgil on Virtual Cage, 2026: a group of figures in a black-and-pink room beneath a pale ceiling, with a hanging chair.'}
for p in posts:
 if p['day']<=14:
  if p.get('shots'):p['asset_ids']=list(dict.fromkeys(s['asset_id'] for s in p['shots']))
  if p.get('slides'):p['asset_ids']=list(dict.fromkeys(s['asset_id'] for s in p['slides']))
  p['alt_text_en']=first_alt[p['day']]
  p['cover_en']=p.get('cover_en',p['title_en'])
  p['voiceover']='None. First 14 days use English on-screen text and planned instrumental music only; no new speech recording required.'
  p['export_tr']='Reel: 1080 × 1920, 30 fps, H.264 MP4, AAC; kompozisyonu sığdır, bütün resmi zorla kırpma. Carousel/tek: 1080 × 1350 JPEG sRGB; bütün ve detayları nötr zemin içinde koru. Bunlar ortak üretim tercihleri; güncel yükleme kabulü yayın ekranında görülür.'
  p['text_layout_tr']='Reelde başlığı x=90–900/y=260–420 nötr alanda tut; ana görüntü y=450–1450. Sağ kontrol bölgesi ve alt arayüz için boşluk bırak. Bunlar kesin platform güvenli alanı değil; son telefon önizlemesi gerekir.'
  p['cover_tr']='İngilizce kapak en çok iki kısa satır; ayrı kapak metni ilk oynayan karenin yerine sayılmaz.'
 else:
  w=works[p['primary_work_key']]
  p['asset_selection_status']='Bütün master seçildi; detaylar ve kaynak video adayları haftalık üretimde konuya göre kesinleştirilir.'
  p['alt_text_en']=f"{w['title']}, {w['year']}, by Yiğit Özen. Full painting and selected close views. Detailed visual alt text to be checked against the final selected frames."
 p['assets']=[{'id':i,'path':assets[i]['path'],'relative_path':assets[i]['relative_path'],'sha256':assets[i].get('sha256'),'role':('recorded_stage' if i in works[p['primary_work_key']]['process'] else 'whole_or_detail')} for i in p['asset_ids']]
 (OUT/p['caption_file']).write_text(p['caption_en']+'\n',encoding='utf-8')

# Sonraki 166 gün için üretim kararları: kaynak/video seçimi ve tek haftalık gözlem.
process_videos={'mandarin':'A0188','wall':'A0280','gary':'A0303','virgil':'A0477','board':'A0928','sept':'A1053','gxd':'A1340','angora':'A1632','capricorn':'A2802','viperella':'A2815'}
video_notes={v['id']:v for v in read(ROOT/'archive-audit/video-notes-complete.json')}
for w in weekly:
 w['primary_video_candidate']=process_videos.get(w['primary'])
 if w['primary_video_candidate']:
  w['video_candidate_note']=video_notes[w['primary_video_candidate']]['description']
  w['video_usage_rule']='Kaynak/yedek aday. İlk 14 günün kesin kartlarına otomatik eklenmez. Uzun anlatımda logo/giriş ve sessiz bekleme çıkarılır; Türkçe konuşma kullanılacaksa elle düzeltilmiş İngilizce altyazı gerekir. Var olan kurgu/ses olduğu gibi yüklenmez.'
for d in days:
 if d.get('post_id'):
  p=next(p for p in posts if p['id']==d['post_id']);d['task']=p['title_en'];d['story']='19:20 · '+p['story_text_en']
 if d['day'] in [14,30,60,90,120,150,180]:d['milestone']='Gerçek takip/erişim/ilgili eser sorusu/üretim süresini ayrı değerlendir; yayın performansı yoksa sonuç alanları boş kalır.'
 if d['day']==180:d['closing_review_time']='23:00';d['measurement_tail_through_day']=187

save(OUT/'works.json',works);save(OUT/'music.json',music)
plan={'schema':'instagram-fourth-leg-180-day-editorial-v1','written_at':'2026-10-28','language':'en','timezone':'Europe/Paris','start_date':None,'day1_definition':'İlk gerçek yayın günü. Hazırlık günleri 180 güne dahil değildir.','status':'planned_not_launched','day_count':180,'feed_count':len(posts),'format_counts':dict(collections.Counter(p['format'].split()[0] for p in posts)),'first_14_days_detailed':True,'advertising':{'active_budget_eur':0,'activation_day':None,'original_90_day_ceiling_eur':390,'extension_budget_approved':False,'rule':'Önce organik yayın ve ilk sonuçlar. Gün 30 yalnız değerlendirme fırsatı; otomatik başlangıç değil. 180 güne uzatma reklam bütçesini ikiye katlamaz.'},'strategy_sources':['../working/plan-gun-1-90.json','../source/instagram/04-strategy/strategy-index-20261016.md','../../archive-audit/ARSIV-AUDIT.html'],'music_selection_basis':'Parça sayfaları ve lisans 28 Ekim 2026 tarihinde okundu. Seçim editoryal öneri; dinlenmiş beat analizi veya trend iddiası değil.','days':days,'weeks':weekly,'posts':posts}
save(OUT/'plan-180.json',plan)
fields=['day','week','time','timezone','format','id','title_en','primary_work_key','asset_ids','duration_seconds','music_id','music_window_seconds','caption_en','edit_tr','story_time','story_text_en','status']
with (OUT/'YAYIN-TAKVIMI-180.csv').open('w',encoding='utf-8-sig',newline='') as f:
 cw=csv.DictWriter(f,fields);cw.writeheader()
 for p in posts:cw.writerow({k:json.dumps(p[k],ensure_ascii=False) if isinstance(p.get(k),(list,dict)) else p.get(k,'') for k in fields})
with (OUT/'GUN-GUN-180.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields2=['day','week','cycle_day','time','is_feed_post','post_id','format','task','story','milestone'];cw=csv.DictWriter(f,fields2,extrasaction='ignore');cw.writeheader();cw.writerows(days)
usage=collections.defaultdict(list)
for p in posts:
 for a in p['asset_ids']:usage[a].append(p['day'])
 for a in [p['story_asset_id']]:usage[a].append(p['day'])
save(OUT/'asset-usage.json',[{'asset_id':i,'source_path':assets[i]['path'],'days':sorted(set(ds)),'use':'editorial_plan_not_exported'} for i,ds in sorted(usage.items())])

# HTML belgeleri: yerel arşiv dosyalarını açar, paylaşım veya harcama yapmaz.
E=lambda s:html.escape(str(s))
def localuri(p):return Path(p).as_uri()
def img(i):return '../../archive-audit/thumbs/'+i+'.jpg.webp'
def source(i):return f'<a href="{E(localuri(assets[i]["path"]))}" title="{E(assets[i]["relative_path"])}">{E(i)} · {E(Path(assets[i]["path"]).name)}</a>'
def gallery(p):return '<div class="assets">'+''.join(f'<a href="{E(localuri(assets[i]["path"]))}"><img loading="lazy" src="{img(i)}" alt="{E(i)}"><span>{E(i)}</span></a>' for i in p['asset_ids'])+'</div>'
def musicline(p):
 m=music[p['music_id']]
 if not m['url']:return 'Müzik yok. Fotoğraf/carousel için bilinçli seçim; sessiz Reel yalnız ses gözlemi haftasında.'
 s,e=p['music_window_seconds'];return f'<a href="{E(m["url"])}">{E(m["title"])} — Scott Buckley</a> · {s//60:02}:{s%60:02}–{e//60:02}:{e%60:02} · {E(m["reason"])}'
def card(p,detailed=False):
 w=works[p['primary_work_key']];parts=[f'<article class="post" id="day-{p["day"]}" data-week="{p["week"]}" data-format="{p["format"].split()[0]}"><div class="eyebrow">Gün {p["day"]} · {p["time"]} Paris · {E(p["format"])} · {"Ayrıntılı plan" if detailed else "Taslak"}</div><h3>{E(p["title_en"])}</h3><p class="muted">{E(w["title"])} · {w["year"]}</p>',gallery(p),f'<p><b>Nasıl:</b> {E(p["edit_tr"])}</p><p><b>Ses:</b> {musicline(p)}</p>']
 if detailed:
  if p.get('shots'):
   parts.append('<h4>Saniyeli kurgu ve ekranda yazacak metin</h4><table><thead><tr><th>Zaman</th><th>Kaynak</th><th>On-screen text</th><th>Uygulama</th></tr></thead><tbody>')
   for s in p['shots']:parts.append(f'<tr><td>{s["start"]}–{s["end"]} sn</td><td>{source(s["asset_id"])}</td><td class="english">{E(s["on_screen_en"])}</td><td>{E(s["edit_tr"])}</td></tr>')
   parts.append('</tbody></table>')
  if p.get('slides'):
   parts.append('<h4>Carousel sayfaları</h4><table><thead><tr><th>Sayfa</th><th>Kaynak</th><th>Slide text</th><th>Düzen</th></tr></thead><tbody>')
   for s in p['slides']:parts.append(f'<tr><td>{s["page"]}</td><td>{source(s["asset_id"])}</td><td class="english">{E(s["text_en"])}</td><td>{E(s["layout_tr"])}</td></tr>')
   parts.append('</tbody></table>')
  parts.append(f'<p><b>Export:</b> {E(p["export_tr"])}</p><p><b>Yerleşim:</b> {E(p["text_layout_tr"])}</p><p><b>Voiceover:</b> {E(p["voiceover"])}</p>')
 elif p.get('slide_texts_en'):parts.append('<p><b>Sayfa sırası:</b> '+' → '.join(E(s) for s in p['slide_texts_en'])+'</p>')
 if not detailed:parts.append('<p class="muted">'+E(p['asset_selection_status'])+'</p>')
 parts.append(f'<details {"open" if detailed else ""}><summary>English caption · kopyalanabilir metin</summary><pre>{E(p["caption_en"])}</pre><a class="button" href="{E(p["caption_file"])}">Caption dosyası</a></details>')
 parts.append(f'<p><b>Story · {p["story_time"]}:</b> <span lang="en">{E(p["story_text_en"])}</span> · {source(p["story_asset_id"])}</p>')
 if detailed:parts.append(f'<p>{E(p["story_action"])}</p><p><b>Alt text:</b> <span lang="en">{E(p["alt_text_en"])}</span></p>')
 parts.append(f'<p class="muted">Ölçüm: yayından 24/72/168 saat sonra. Öncelik: {E(p["primary_metric"])}. Medya dosyası henüz renderlenmedi.</p></article>');return ''.join(parts)
style='''*{box-sizing:border-box}body{margin:0;background:#f4f1e9;color:#24231f;font:16px/1.6 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:35px 24px 80px}h1{font-size:clamp(30px,5vw,56px);line-height:1.12;max-width:900px}h2{margin-top:48px;font-size:29px}h3{font-size:24px;line-height:1.3;margin:12px 0}h4{margin-top:28px}.lead{font-size:19px;max-width:920px}.muted{color:#67655b;font-size:14px}a{color:#254f58;text-underline-offset:3px}.post,section.panel{background:#fffdf7;border:1px solid #d9d2c2;padding:28px;border-radius:12px;margin:20px 0;overflow:auto}.eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:.07em;color:#7b4c31}.assets{display:flex;gap:12px;overflow:auto;padding:10px 0}.assets a{flex:0 0 145px;text-decoration:none;font-size:12px}.assets img{width:145px;height:155px;object-fit:contain;background:#eae6dc;display:block;border-radius:4px}.assets span{display:block;margin-top:5px}table{border-collapse:collapse;width:100%;font-size:14px;margin:15px 0}td,th{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #ddd5c5}th{background:#eee9dc}.english{white-space:pre-line;min-width:160px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f1e9;padding:20px;border-radius:6px;font:15px/1.7 system-ui,sans-serif}summary{cursor:pointer;font-weight:650;margin:12px 0}nav{display:flex;gap:14px;flex-wrap:wrap;margin:25px 0}.button,nav a{display:inline-block;padding:7px 12px;border:1px solid #bcb5a5;border-radius:5px;text-decoration:none}.stats{display:flex;gap:14px;flex-wrap:wrap}.stat{background:#e8e4d6;padding:18px;min-width:155px;border-radius:8px}.stat b{display:block;font-size:29px}.notice{border-left:4px solid #9f6b43;padding:12px 20px;background:#ece5d6}.tools{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#f4f1e9ed;padding:12px;z-index:2;border-bottom:1px solid #d0c8b9}select,input{font:inherit;max-width:100%;padding:8px;background:#fffdf7;border:1px solid #bcb5a5;border-radius:4px}label{font-size:13px}.hidden{display:none!important}@media(max-width:650px){main{padding:22px 14px}.post,section.panel{padding:17px}table{min-width:650px}.stats{gap:7px}.stat{min-width:130px;padding:12px}.assets a,.assets img{width:125px;flex-basis:125px}.assets img{height:130px}}@media print{.tools,nav{display:none}details{display:block}article{break-inside:avoid}body{background:white}}'''
intro=f'''<p class="eyebrow">yigitozen.art · Ayak 4 · yerel yayın planı</p><h1>180 günlük seçki ve yayın planı</h1><p class="lead">Gün 1 ilk gerçek yayın günü. İlk 14 gün ayrıntılı üretim kartlarıyla hazırlandı; Gün 15–180 haftalık sonuçlara göre yenilenecek taslak seçkidir. Tüm izleyici metinleri İngilizce; uygulama notları Türkçe.</p><div class="stats"><div class="stat"><b>180</b>gün</div><div class="stat"><b>129</b>akış yayını</div><div class="stat"><b>77 / 26 / 26</b>Reel / carousel / tek</div><div class="stat"><b>10</b>ayrıntılı yayın kartı</div></div><p class="notice">Bu bir yayın ve kurgu planı. Medya dosyaları renderlenmedi, Instagram’a yüklenmedi. Reklam başlangıcı ve harcama atanmadı. Kaynak arşiv değişmedi.</p>'''
rules='''<section class="panel" id="principles"><h2>Yayın kararları</h2><p><b>Ritim:</b> Her yedi günlük döngüde 1 Reel, 2 carousel, 3 üretim, 4 Reel, 5 tam eser, 6 ilişkili eser Reel’i, 7 değerlendirme. Gün 176–180 son kısmi döngüdür; gün 181’e taşan Reel bu plana eklenmedi.</p><p><b>Saat:</b> Akış 19.00, destek Story 19.20, üretim/değerlendirme 18.00; Europe/Paris yerel saati. 19.00 bir başlangıç denemesi. İlk dört hafta sabit; sonrasında içerik testiyle birlikte saat değiştirilmez. Gün 1’in haftanın hangi günü olduğu şimdiden varsayılmaz.</p><p><b>Seçki:</b> Arşivdeki her dosya paylaşılmaz. Aynı resmin çözünürlük kopyaları, efekt sürümleri, düşük kalite katalog türevleri, kimlik/kişisel yazışmalar ve doğrulanmamış sentetik sunumlar seçkiyi şişirmez. Aynı esere dönüş, farklı görünür kanıt ve farklı soru taşımalıdır. Kullanılan dosyalar asset-usage.json içinde gün bazında bağlıdır.</p><p><b>Görüntü:</b> Hazır seçili detaylardan ve hizalanmış gerçek süreç fotoğraflarından yararlanılır. Slayt/geçiş, canlı boyama videosu gibi adlandırılmaz. Tarihli işler kendi gerçek yıllarıyla sunulur. Yapay mekân/ölçek ve sahte önce/sonra yok.</p><p><b>İngilizce:</b> Caption, kapak, ekran yazısı, Story ve ilk iki haftanın alt metni İngilizce. İlk 14 günde konuşma gerekmiyor. Sonraki Türkçe anlatım adaylarında otomatik ham döküm doğrudan altyazı yapılmaz.</p><p><b>Müzik:</b> Beş parçalık sabit enstrümantal seçki; her Reel’e parça ve bölüm atandı. Fotoğraf ve carousel bilinçli olarak müziksiz. Zaman bölümleri kurgu önerisidir; parçalar bu görevde dinlenmedi ve vuruş işaretleri çıkarılmadı. Son eşleştirme ilk render sırasında dinlenerek yapılır. 77 Reel’in müziğinin ayrı ayrı trend olması varsayılmaz.</p><p><b>Reklam:</b> Önce organik yayın ve ölçüm. Gün 30’da değerlendirme yapılabilir; başlangıç emri değildir. 390 € önceki 90 günlük üst çerçeve olarak kalır; 180 güne uzatma 780 € onayı değildir. Organik ölçüm çiftleri desteklenirse ücretli etki ayrı işaretlenir.</p><p><b>Yük:</b> İki hafta art arda eser üretimini aksatırsa yalnız döngü 1 Reel, 2 carousel, 5 tam eser kalır; atlananlar ertesi güne yığılmaz. Sonraki taslaklar görev değişimini kaydederek ötelenir.</p></section>'''
profile='''<section class="panel" id="profile"><h2>Gün 1 öncesi profil girişi</h2><p>İngilizce bio taslağı:</p><pre>Paintings by Yiğit Özen\nBodies, familiar scenes and unstable spaces.\nSelected works ↓</pre><p>Seçki bağlantısı yayımdan önce gerçekten açılıp kontrol edilmeli. Gün 1 Reel’i giriş, Gün 2 carousel’i inceleme, Gün 5 tam eser künyeli sunum işleviyle ilk üç sabit içerik adayıdır. Sabitleme, bu yayınlar gerçekten çıktıktan sonra yapılır.</p><p>Başlangıçta takipçi ve mevcut performansı kaydet. Tarih, teknik ve ölçüler yerel katalog/yayın kayıtlarına bağlıdır; fiyat, müsaitlik ve temsil bilgisi eklenmedi. Painstaking soldan sağa A0028 → A0029 → A0027; panel dosyalarının alfabetik sırası kullanılmaz.</p></section>'''
measurement='''<section class="panel" id="review"><h2>Ölçüm ve taslağı yenileme</h2><p>Her gönderide gerçek yayından 24/72/168 saat sonra erişim, izlenme süresi mevcutsa, paylaşım, kaydetme, profil ziyareti, gönderiye atfedilen takip mevcutsa ve esere özgü sorular ayrı kaydedilir. Görünmeyen veri N/A kalır. Üretim dakikası da yazılır.</p><p>Gün 14 iş yükü; Gün 30 ilk anlaşılma ve profil devamı; Gün 60 tekrar edilebilirlik; Gün 90 ilk dönem sonucu; Gün 120 ve 150 farklı esere aktarım; Gün 180 dönem kapanışı. Son gönderilerin yedi günlük ölçümü Gün 187’ye uzanır.</p><p>Gün 15–28: ilk haftalardaki vaat anlaşılmıyorsa yalnız ilk görüntü/metin bağı düzeltilir. Gün 29–90: stratejideki carousel, paylaşma, ses, başlık ve profil deneyleri tek tek yürür. Gün 91–180: işe yarayan ilke yeni esere taşınır; her hafta yeni bir numara aranmaz.</p><p>D08 ile D13 farklı eserlerdir; giriş sırası için temiz A/B değildir. D43/D46 ses gözlemi de farklı detayların etkisini içerir. Güçlü neden-sonuç veya “algoritma oturdu” hükmü üretmeyiz. Haftalık performans yoksa geleceğin kazanan eseri ilan edilmez.</p></section>'''
musicpanel='<section class="panel" id="music"><h2>Müzik kaynakları</h2><p>Bestecinin parça sayfaları ticari projeler dahil CC BY 4.0 kullanımını atıf koşuluyla açıklıyor. Gerekli parça/kredi bağlantısı her müzikli caption’a eklendi. Instagram kataloğu erişimi veya otomatik hak tanıması denenmedi. Kaynak MP3 kurguda kullanılacak; platformdan rastgele aynı adlı ses seçilmeyecek.</p><ul>'+''.join(f'<li>{k}: <a href="{E(m["url"])}">{E(m["title"])}</a> — {E(m["reason"])}</li>' for k,m in music.items() if m['url'])+'</ul><p><a href="https://www.scottbuckley.com.au/library/faq/">Bestecinin kullanım açıklaması</a> · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Kaynaklar 28 Ekim 2026 tarihinde okundu.</p></section>'
preparation='''<section class="panel" id="prep"><h2>İlk iki haftanın hazırlığı</h2><p>Gün 0: başlangıç ölçümü ve portföy girişi; on yayının kaynaklarını aşağıdaki kartlardan topla. İlk beş yayını sırayla D001, D002, D004, D005, D006 adlarıyla export et. Gün 3’te ikinci haftanın D008, D009, D011, D012, D013 dosyalarını bitir; gün 10’da üçüncü hafta taslağını ilk sonuçlarla gözden geçir.</p><p>Gün 3 ve 10 saat 18.00 üretim; Gün 7 ve 14 saat 18.00 değerlendirme. Gerçek yaş ölçümleri yayın saatine göre alınır; örneğin Gün 1’in 72 saat ölçümü Gün 4 saat 19.00’dır.</p><p>İlk hafta detayları hazır seçilmiş kaynaktan alınır. İkinci hafta Angora detaylarının kadraj dışında kalan ahşap çekim çevresi çıkarılır; boyalı alanın perspektifini yeniden bozma. FRAMED sırası 0, 1, 2…10, 12, 13, 14; 11 dosyası bu dizide yok, ara aşama uydurulmaz.</p></section>'''
def header(title):return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{style}</style></head><body><main>'
nav='<nav><a href="ILK-14-GUN.html">İlk 14 gün ayrıntılı</a><a href="YAYIN-TAKVIMI-180.csv">129 yayın CSV</a><a href="GUN-GUN-180.csv">180 gün görev CSV</a><a href="plan-180.json">Tüm plan JSON</a><a href="../../archive-audit/ARSIV-AUDIT.html">Arşiv audit</a></nav>'
doc=header('Instagram 180 günlük yayın planı')+intro+nav+rules+profile+measurement+musicpanel
doc+='<section class="panel" id="overview"><h2>Seçkinin 26 haftalık omurgası</h2><table><thead><tr><th>Hafta / gün</th><th>İlk eser → ilişkili eser</th><th>Haftanın sorusu</th><th>Ses</th></tr></thead><tbody>'
for w in weekly:
 lo,hi=w['day_range'];a=works[w['primary']];b=works[w['related']]
 doc+=f'<tr><td><a href="#day-{lo}">{w["week"]} / {lo}–{hi}</a></td><td>{E(a["title"])} ({a["year"]}) → {E(b["title"])} ({b["year"]})</td><td>{E(w["theme"])}</td><td>{E(music[w["music_id"]]["title"])}</td></tr>'
doc+='</tbody></table></section>'
doc+='<h2 id="calendar">26 haftalık yayın kartları</h2><div class="tools"><label>Hafta <select id="week"><option value="all">Tümü</option>'+''.join(f'<option value="{i}">{i}</option>' for i in range(1,27))+'</select></label><label>Format <select id="format"><option value="all">Tümü</option><option>Reel</option><option>Carousel</option><option>Single</option></select></label><label>Ara <input id="search" placeholder="Eser, gün veya konu"></label><span id="count"></span></div>'
for w in weekly:
 a=works[w['primary']];b=works[w['related']];lo,hi=w['day_range']
 doc+=f'<section class="week" data-week="{w["week"]}"><h2>Hafta {w["week"]} · Gün {lo}–{hi}</h2><p><b>{E(w["theme"])}</b><br>{E(a["title"])} ({a["year"]}) → {E(b["title"])} ({b["year"]})</p><p class="muted">{E(w["learning_question"])} {E(w["controls"])}</p>'
 for p in posts:
  if p['week']==w['week']:doc+=card(p,p['day']<=14)
 doc+='</section>'
doc+='''<script>const W=document.querySelector('#week'),F=document.querySelector('#format'),S=document.querySelector('#search');function filter(){let n=0;document.querySelectorAll('.post').forEach(p=>{let ok=(W.value==='all'||p.dataset.week===W.value)&&(F.value==='all'||p.dataset.format===F.value)&&(!S.value||p.innerText.toLowerCase().includes(S.value.toLowerCase()));p.classList.toggle('hidden',!ok);if(ok)n++});document.querySelectorAll('.week').forEach(w=>w.classList.toggle('hidden',![...w.querySelectorAll('.post')].some(p=>!p.classList.contains('hidden'))));document.querySelector('#count').textContent=n+' yayın';}W.onchange=F.onchange=S.oninput=filter;filter();</script></main></body></html>'''
(OUT/'PLAN-180.html').write_text(doc,encoding='utf-8')
doc=header('Instagram ilk 14 gün ayrıntılı yayın planı')+intro.replace('180 günlük seçki ve yayın planı','İlk 14 gün ayrıntılı yayın planı')+'<nav><a href="PLAN-180.html">180 günlük ana plana dön</a><a href="YAYIN-TAKVIMI-180.csv">Yayın CSV</a></nav>'+preparation+profile
doc+='<section class="panel"><h2>İlk 14 gün hızlı takvim</h2><table><thead><tr><th>Gün</th><th>Saat</th><th>Görev</th><th>Eser / konu</th></tr></thead><tbody>'
for d in days[:14]:
 href=f'<a href="#day-{d["day"]}">{d["day"]}</a>' if d['is_feed_post'] else str(d['day'])
 doc+=f'<tr><td>{href}</td><td>{E(d["time"])}</td><td>{E(d.get("format","Üretim" if d["cycle_day"]==3 else "Değerlendirme"))}</td><td>{E(d["task"])}</td></tr>'
doc+='</tbody></table></section>'
for p in posts:
 if p['day']<=14:doc+=card(p,True)
doc+=musicpanel+measurement+'</main></body></html>'
(OUT/'ILK-14-GUN.html').write_text(doc,encoding='utf-8')

# Gerçekleşmiş ölçüm yok; alanlar boş ve organik/ücretli ayrımı korunuyor.
save(OUT/'measurement-log.json',{'baseline_followers':None,'baseline_measured_at':None,'entries':[{'post_id':p['id'],'planned_day':p['day'],'actual_published_at':None,'production_minutes':None,'paid_spend_eur':None,'observations':[{'age_hours':h,'measured_at':None,'reach':None,'views':None,'watch_seconds':None,'shares':None,'saves':None,'profile_visits':None,'attributed_follows':None,'work_specific_questions':None,'notes':None} for h in [24,72,168]]} for p in posts]})

errors=[]
assert len(days)==180 and len(posts)==129
assert collections.Counter(p['format'].split()[0] for p in posts)=={'Reel':77,'Carousel':26,'Single':26}
for p in posts:
 assert len(p['caption_en'])<2200,(p['day'],len(p['caption_en']))
 for a in p['assets']:
  if not Path(a['path']).exists():errors.append(a['path'])
 if p.get('shots'):
  assert p['shots'][0]['start']==0 and p['shots'][-1]['end']==p['duration_seconds']
  assert all(a['end']==b['start'] for a,b in zip(p['shots'],p['shots'][1:]))
 assert assets[p['story_asset_id']]['kind']=='image'
 for a in p['asset_ids']:assert assets[a]['kind']=='image'
assert not errors,errors
validation={'valid':True,'days':180,'posts':129,'reels':77,'carousels':26,'single_images':26,'detailed_posts':10,'unique_works':len(set(k for p in posts for k in p['work_keys'])),'unique_selected_assets':len(usage),'all_source_paths_exist':True,'captions_under_2200_characters':True,'detailed_timelines_contiguous':True,'actual_publications':0,'active_ad_budget_eur':0,'media_rendered':False,'caption_language':'English','unreviewed_music_detail':'Parça bölümleri plan önerisi; işitsel/vuruş eşleştirmesi render aşamasında.','completed_scope':'180 gün taslak ve ilk 14 gün ayrıntılı editoryal plan'}
save(OUT/'validation.json',validation)
print(json.dumps(validation,ensure_ascii=False))
