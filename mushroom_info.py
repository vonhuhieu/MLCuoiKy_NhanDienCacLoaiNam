"""
Từ Điển Tri Thức 44 Loài Nấm (Mushroom Knowledge Base)
Bao gồm:
- Tên khoa học (Scientific Name)
- Tên tiếng Việt thông dụng
- Mức độ độc tính (Edibility: 'edible', 'toxic', 'inedible', 'caution')
- Phân loại tiếng Việt
- Mô tả đặc điểm nhận dạng & môi trường sống
- Triệu chứng ngộ độc / Công dụng
"""

MUSHROOM_INFO = {
    "Agaricus augustus": {
        "scientific_name": "Agaricus augustus",
        "vn_name": "Nấm mỡ hoàng tử (The Prince)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Ngon)",
        "toxicity_level": "none",
        "description": "Nấm lớn, có mùi thơm như quả hạnh nhân hoặc hoa hồi, mũ nấm có vảy màu nâu vàng.",
        "habitat": "Thường mọc dưới các gốc thông hoặc ven đường rừng hỗn giao."
    },
    "Amanita amerirubescens": {
        "scientific_name": "Amanita amerirubescens",
        "vn_name": "Nấm tán đỏ Mỹ (Blusher)",
        "edibility": "caution",
        "edibility_vn": "Cần cẩn trọng (Phải nấu chín kỹ)",
        "toxicity_level": "mild_when_raw",
        "description": "Thịt nấm chuyển sang màu ửng đỏ khi bị xước hoặc dập. Chứa độc tố tan máu khi ăn sống, chỉ an toàn khi nấu chín kỹ.",
        "habitat": "Mọc cộng sinh với cây sồi, thông trong rừng cây lá rộng."
    },
    "Amanita brunnescens": {
        "scientific_name": "Amanita brunnescens",
        "vn_name": "Nấm tán nâu hình sao",
        "edibility": "toxic",
        "edibility_vn": "Có độc",
        "toxicity_level": "moderate",
        "description": "Mũ nấm màu nâu xám, gốc củ có các vết nứt dọc đặc trưng dạng khe rãnh.",
        "habitat": "Mọc đơn lẻ hoặc thành cụm nhỏ trong rừng sồi, thông."
    },
    "Amanita calyptroderma": {
        "scientific_name": "Amanita calyptroderma",
        "vn_name": "Nấm mũ áo choàng mỏng",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Rất ngon)",
        "toxicity_level": "none",
        "description": "Mũ nấm màu vàng cam hoặc nâu vàng, thường mang một mảng bao chung lớn màu trắng ở đỉnh mũ.",
        "habitat": "Phổ biến ở bờ Tây Bắc Mỹ, mọc dưới tán sồi và cây lá kim."
    },
    "Amanita flavoconia": {
        "scientific_name": "Amanita flavoconia",
        "vn_name": "Nấm tán vảy vàng",
        "edibility": "toxic",
        "edibility_vn": "Nghi ngờ có độc / Độc",
        "toxicity_level": "moderate",
        "description": "Mũ nấm màu vàng tươi đến cam, phủ các đốm bột màu vàng lưu huỳnh.",
        "habitat": "Mọc trên đất rừng nhiều mùn, cộng sinh với cây lá kim và sồi."
    },
    "Amanita muscaria": {
        "scientific_name": "Amanita muscaria",
        "vn_name": "Nấm tán bay / Nấm ruồi (Fly Agaric)",
        "edibility": "toxic",
        "edibility_vn": "Độc (Gây ảo giác & rối loạn thần kinh)",
        "toxicity_level": "high",
        "description": "Biểu tượng nấm kinh điển: Mũ đỏ tươi phủ vảy trắng đốm. Chứa acid ibotenic và muscimol gây ngộ độc thần kinh.",
        "habitat": "Rừng thông, rừng bạch dương vùng ôn đới."
    },
    "Amanita velosa": {
        "scientific_name": "Amanita velosa",
        "vn_name": "Nấm tán cam mùa xuân",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Hảo hạng)",
        "toxicity_level": "none",
        "description": "Mũ màu hồng đào đến cam nhạt, mép khía rõ, không có vòng bao ở thân, gốc có bao chung dạng túi sâu.",
        "habitat": "Mọc vào mùa xuân dưới gốc sồi."
    },
    "Armillaria mellea": {
        "scientific_name": "Armillaria mellea",
        "vn_name": "Nấm mật ong (Honey Mushroom)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Nấu kỹ)",
        "toxicity_level": "mild_when_raw",
        "description": "Mũ màu vàng mật ong, mọc thành chùm lớn quanh gốc cây mục. Ăn sống có thể gây khó chịu dạ dày.",
        "habitat": "Ký sinh và hoại sinh trên các thân gỗ mục, gốc cây."
    },
    "Armillaria tabescens": {
        "scientific_name": "Armillaria tabescens",
        "vn_name": "Nấm mật không vòng",
        "edibility": "edible",
        "edibility_vn": "Ăn được",
        "toxicity_level": "none",
        "description": "Tương tự nấm mật ong nhưng thân nấm không có vòng đệm (ringless). Mọc thành cụm rậm rạp.",
        "habitat": "Quanh gốc cây mục hoặc rễ cây ngầm."
    },
    "Artomyces pyxidatus": {
        "scientific_name": "Artomyces pyxidatus",
        "vn_name": "Nấm san hô hình vương miện",
        "edibility": "edible",
        "edibility_vn": "Ăn được",
        "toxicity_level": "none",
        "description": "Hình dáng như nhánh san hô phân nhánh, đầu mỗi nhánh hình cái chén nhỏ như vương miện.",
        "habitat": "Mọc trực tiếp trên các khúc gỗ mục ẩm ướt trong rừng."
    },
    "Bolbitius titubans": {
        "scientific_name": "Bolbitius titubans",
        "vn_name": "Nấm mũ vàng nhầy",
        "edibility": "inedible",
        "edibility_vn": "Không ăn được (Thịt mỏng)",
        "toxicity_level": "none",
        "description": "Mũ nấm màu vàng sáng lúc non, sau chuyển sang xám nhạt có khía, bề mặt nhớt nhầy, thịt rất mỏng manh.",
        "habitat": "Mọc trên phân mục hoặc bãi cỏ ẩm giàu dinh dưỡng."
    },
    "Boletus pallidus": {
        "scientific_name": "Boletus pallidus",
        "vn_name": "Nấm gan bò nhợt",
        "edibility": "edible",
        "edibility_vn": "Ăn được",
        "toxicity_level": "none",
        "description": "Mũ màu xám trắng đến vàng nhạt, lớp lỗ xốp dưới mũ ngả xanh lam khi bị cọ xát hoặc cắt.",
        "habitat": "Mọc dưới cây sồi và rừng hỗn giao."
    },
    "Boletus rex-veris": {
        "scientific_name": "Boletus rex-veris",
        "vn_name": "Nấm vua mùa xuân (Spring King Bolete)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Hảo hạng)",
        "toxicity_level": "none",
        "description": "Nấm lớn, thịt dày chắc, mũ nâu đỏ bóng, vị ngọt bùi giá trị ẩm thực rất cao.",
        "habitat": "Mọc ven rừng lá kim trên núi cao vào mùa xuân."
    },
    "Cantharellus californicus": {
        "scientific_name": "Cantharellus californicus",
        "vn_name": "Nấm mồng gà khổng lồ California",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Hảo hạng)",
        "toxicity_level": "none",
        "description": "Có hình phễu màu vàng mơ, thịt dày thơm mùi quả đào/mơ, là loài nấm mồng gà lớn nhất thế giới.",
        "habitat": "Cộng sinh với cây sồi ven bờ biển California."
    },
    "Cantharellus cinnabarinus": {
        "scientific_name": "Cantharellus cinnabarinus",
        "vn_name": "Nấm mồng gà đỏ chu sa",
        "edibility": "edible",
        "edibility_vn": "Ăn được",
        "toxicity_level": "none",
        "description": "Kích thước nhỏ nhắn, nổi bật với màu đỏ hồng đến đỏ cam rực rỡ như chu sa.",
        "habitat": "Mọc trên nền rừng sồi và rừng rụng lá."
    },
    "Cerioporus squamosus": {
        "scientific_name": "Cerioporus squamosus",
        "vn_name": "Nấm yên ngựa gỗ (Dryad's Saddle)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Khi còn non)",
        "toxicity_level": "none",
        "description": "Hình dáng quạt lớn xòe ngang thân cây gỗ, mặt trên có vảy nâu sẫm, khi non có mùi dưa chuột mát.",
        "habitat": "Mọc trên thân cây gỗ rụng lá mục hoặc sống."
    },
    "Clitocybe nuda": {
        "scientific_name": "Clitocybe nuda",
        "vn_name": "Nấm hương tím (Wood Blewit)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Nấu chín)",
        "toxicity_level": "mild_when_raw",
        "description": "Mũ và phiến nấm có màu tím hoa cà rất đẹp, hương thơm nhẹ, ăn sống dễ gây dị ứng tiêu hóa.",
        "habitat": "Mọc trên lớp thảm lá mục hoặc đống phân ủ mục nát."
    },
    "Coprinellus micaceus": {
        "scientific_name": "Coprinellus micaceus",
        "vn_name": "Nấm mực vảy óng ánh",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Nấu ngay)",
        "toxicity_level": "none",
        "description": "Mũ nấm hình chuông màu nâu nhạt, phủ các hạt lấp lánh như vảy mica, tự chảy rữa thành mực đen khi già.",
        "habitat": "Mọc thành cụm quanh gốc cây mục mục ruỗng."
    },
    "Coprinus comatus": {
        "scientific_name": "Coprinus comatus",
        "vn_name": "Nấm mực lông gà (Shaggy Mane)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Ngon khi non)",
        "toxicity_level": "none",
        "description": "Mũ thon dài phủ vảy xù xì màu trắng, thịt mềm ngọt nhưng phải chế biến ngay trước khi nấm tự hóa lỏng thành mực.",
        "habitat": "Bãi cỏ, ven đường, công viên đất mùn ẩm."
    },
    "Daedaleopsis confragosa": {
        "scientific_name": "Daedaleopsis confragosa",
        "vn_name": "Nấm vân gỗ mê lộ",
        "edibility": "inedible",
        "edibility_vn": "Không ăn được (Thớ gỗ cứng dai)",
        "toxicity_level": "none",
        "description": "Nấm dạng dĩa bám thân gỗ, mặt dưới lỗ xếp như hình mê cung, thể quả hóa gỗ cứng dai.",
        "habitat": "Mọc trên các cành bạch dương, liễu mục."
    },
    "Entoloma abortivum": {
        "scientific_name": "Entoloma abortivum",
        "vn_name": "Nấm thợ săn tôm non (Shrimp Mushroom)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Ngon)",
        "toxicity_level": "none",
        "description": "Thường gặp ở dạng biến dạng màu trắng xốp như viên bỏng ngô do ký sinh lên nấm mật ong, vị giòn ngọt.",
        "habitat": "Rừng lá rộng nhiều cây mục ẩm ướt."
    },
    "Flammulina velutipes": {
        "scientific_name": "Flammulina velutipes",
        "vn_name": "Nấm kim châm hoang dã",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Rất phổ biến)",
        "toxicity_level": "none",
        "description": "Dạng hoang dã có mũ màu vàng nâu nhớt, chân nhung đen sẫm, khác với dạng nấm kim châm trắng nuột nuôi cấy.",
        "habitat": "Mọc trên thân cây gỗ mục mùa lạnh."
    },
    "Ganoderma applanatum": {
        "scientific_name": "Ganoderma applanatum",
        "vn_name": "Nấm linh chi tán phẳng / Nấm bảng vẽ họa sĩ",
        "edibility": "inedible",
        "edibility_vn": "Không ăn được (Dược liệu/Nghệ thuật)",
        "toxicity_level": "none",
        "description": "Thể quả gỗ cứng như đá xòe quạt to, mặt dưới trắng mịn cào vẽ được tranh, dùng sắc thuốc uống.",
        "habitat": "Ký sinh sống dai nhiều năm trên thân gỗ già."
    },
    "Grifola frondosa": {
        "scientific_name": "Grifola frondosa",
        "vn_name": "Nấm khiêu vũ / Nấm Maitake",
        "edibility": "edible",
        "edibility_vn": "Ăn được & Dược liệu quý",
        "toxicity_level": "none",
        "description": "Cụm nấm lớn gồm hàng trăm mũ nhỏ màu nâu xám xòe lớp lang như váy múa, tăng cường miễn dịch.",
        "habitat": "Dưới gốc cây sồi cổ thụ."
    },
    "Hericium coralloides": {
        "scientific_name": "Hericium coralloides",
        "vn_name": "Nấm hầu thủ san hô",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Hảo hạng)",
        "toxicity_level": "none",
        "description": "Hình dáng tuyệt đẹp như san hô trắng tinh khiết rủ các sợi gai nhọn, thịt thơm ngọt thanh.",
        "habitat": "Mọc trên các thân gỗ phong, sồi mục rụng."
    },
    "Hygrophoropsis aurantiaca": {
        "scientific_name": "Hygrophoropsis aurantiaca",
        "vn_name": "Nấm mồng gà giả (False Chanterelle)",
        "edibility": "caution",
        "edibility_vn": "Cần thận trọng (Có thể đau bụng)",
        "toxicity_level": "mild",
        "description": "Dễ nhầm với nấm mồng gà ăn được nhưng phiến mỏng rẽ đôi và mũ màu cam rực rỡ hơn.",
        "habitat": "Rừng cây lá kim trên lớp mùn thông mục."
    },
    "Hypholoma fasciculare": {
        "scientific_name": "Hypholoma fasciculare",
        "vn_name": "Nấm đầu lưu huỳnh (Sulfur Tuft)",
        "edibility": "toxic",
        "edibility_vn": "ĐỘC NGUY HIỂM",
        "toxicity_level": "high",
        "description": "Mọc thành chùm lớn màu vàng lưu huỳnh rực rỡ, vị rất đắng. Chứa fasciculol gây nôn ói và tổn thương gan.",
        "habitat": "Mọc dày đặc trên gốc và thân gỗ mục rữa."
    },
    "Hypomyces lactifluorum": {
        "scientific_name": "Hypomyces lactifluorum",
        "vn_name": "Nấm tôm hùm (Lobster Mushroom)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Đặc sản quý)",
        "toxicity_level": "none",
        "description": "Nấm ký sinh phủ lớp vỏ ngoài màu đỏ cam như mai tôm hùm luộc chín, vị giòn ngọt hương hải sản.",
        "habitat": "Ký sinh lên nấm Russula hoặc Lactarius trong rừng thông."
    },
    "Ischnoderma resinosum": {
        "scientific_name": "Ischnoderma resinosum",
        "vn_name": "Nấm da gỉ nhựa",
        "edibility": "edible",
        "edibility_vn": "Ăn được khi non",
        "toxicity_level": "none",
        "description": "Khi còn non tiết ra các giọt chất lỏng màu hổ phách ở mép nấm, thịt mềm có thể chế biến như thịt bò.",
        "habitat": "Thân gỗ cứng mục rụng."
    },
    "Laetiporus sulphureus": {
        "scientific_name": "Laetiporus sulphureus",
        "vn_name": "Nấm gà rừng (Chicken of the Woods)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Thơm ngon như thịt gà)",
        "toxicity_level": "none",
        "description": "Xòe nhiều tầng màu vàng cam rực rỡ, xào nướng vị xé thớ như ức gà. Lưu ý một số người dị ứng nhẹ.",
        "habitat": "Mọc trên thân cây sồi già hoặc cây gỗ lá rộng."
    },
    "Lycoperdon perlatum": {
        "scientific_name": "Lycoperdon perlatum",
        "vn_name": "Nấm trứng ngọc trai (Gem-studded Puffball)",
        "edibility": "edible",
        "edibility_vn": "Ăn được khi ruột còn trắng tinh",
        "toxicity_level": "none",
        "description": "Thân hình con quay tròn phủ gai hạt ngọc, ăn được khi bên trong trắng mịn như đậu phụ.",
        "habitat": "Đất rừng, ven đường mòn ẩm."
    },
    "Lycoperdon pyriforme": {
        "scientific_name": "Lycoperdon pyriforme",
        "vn_name": "Nấm trứng hình quả lê",
        "edibility": "edible",
        "edibility_vn": "Ăn được khi còn non",
        "toxicity_level": "none",
        "description": "Hình dáng giống quả lê nhỏ, mọc thành bầy dày đặc trên thân gỗ mục.",
        "habitat": "Trên các khúc gỗ mục rữa trong rừng ẩm."
    },
    "Mycena haematopus": {
        "scientific_name": "Mycena haematopus",
        "vn_name": "Nấm tiên mũ máu (Bleeding Fairy Helmet)",
        "edibility": "inedible",
        "edibility_vn": "Không ăn được",
        "toxicity_level": "none",
        "description": "Nấm nhỏ thanh mảnh, khi thân bị gãy sẽ ứa ra giọt dịch màu đỏ thẫm như máu.",
        "habitat": "Mọc trên cành mục ẩm ướt."
    },
    "Omphalotus illudens": {
        "scientific_name": "Omphalotus illudens",
        "vn_name": "Nấm đèn lồng ma (Jack-o'-Lantern)",
        "edibility": "toxic",
        "edibility_vn": "ĐỘC (Gây ảo giác & đau bụng nặng)",
        "toxicity_level": "high",
        "description": "Màu cam rực rỡ, phiến nấm phát quang sinh học màu lục trong bóng tối. Rất dễ nhầm với nấm mồng gà.",
        "habitat": "Gốc cây sồi mục thành từng cụm lớn."
    },
    "Omphalotus olivascens": {
        "scientific_name": "Omphalotus olivascens",
        "vn_name": "Nấm đèn lồng ô-liu bờ Tây",
        "edibility": "toxic",
        "edibility_vn": "ĐỘC",
        "toxicity_level": "high",
        "description": "Tương tự nấm đèn lồng ma nhưng có sắc xanh lục ô-liu pha cam, chứa độc tố illudin gây buồn nôn, co thắt dạ dày.",
        "habitat": "Mọc quanh gốc cây sồi và bạch đàn ở California."
    },
    "Phlebia tremellosa": {
        "scientific_name": "Phlebia tremellosa",
        "vn_name": "Nấm màng nhăn thạch",
        "edibility": "inedible",
        "edibility_vn": "Không ăn được",
        "toxicity_level": "none",
        "description": "Trải dẹt như tấm thạch nhăn nheo bám mặt gỗ, màu cam hồng nhạt, chất thạch dai keo.",
        "habitat": "Mặt dưới cành cây mục rụng."
    },
    "Pleurotus ostreatus": {
        "scientific_name": "Pleurotus ostreatus",
        "vn_name": "Nấm sò / Nấm bào ngư xám",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Ngon & phổ biến)",
        "toxicity_level": "none",
        "description": "Mũ hình vỏ sò màu xám tro, thớ thịt ngọt dai giòn, được nuôi trồng và tiêu thụ rộng rãi.",
        "habitat": "Mọc trên thân cây gỗ mục khắp nơi."
    },
    "Pleurotus pulmonarius": {
        "scientific_name": "Pleurotus pulmonarius",
        "vn_name": "Nấm sò phượng hoàng / Sò trắng",
        "edibility": "edible",
        "edibility_vn": "Ăn được",
        "toxicity_level": "none",
        "description": "Tương tự nấm sò xám nhưng mũ mỏng hơn và có màu trắng ngà hoặc xám nhạt, ưa mùa hè.",
        "habitat": "Mọc trên thân cây gỗ lá rộng vào mùa ấm áp."
    },
    "Psilocybe pelliculosa": {
        "scientific_name": "Psilocybe pelliculosa",
        "vn_name": "Nấm thần tiên / Nấm thức thần màng nhầy",
        "edibility": "toxic",
        "edibility_vn": "ĐỘC / THỨC THẦN (Chất cấm gây ảo giác)",
        "toxicity_level": "hallucinogenic",
        "description": "Mũ nấm hình chuông nhỏ màu nâu caramen, chứa psilocybin gây ảo giác thị giác và thay đổi tâm thần.",
        "habitat": "Ven đường mòn phủ mùn cưa và rêu trong rừng cây lá kim."
    },
    "Retiboletus ornatipes": {
        "scientific_name": "Retiboletus ornatipes",
        "vn_name": "Nấm gan bò chân ren vàng",
        "edibility": "inedible",
        "edibility_vn": "Không ăn được (Vị đắng chát)",
        "toxicity_level": "none",
        "description": "Chân nấm có hoa văn vân lưới dập nổi màu vàng chanh rất đẹp nhưng thịt nấm cực kỳ đắng.",
        "habitat": "Rừng sồi và rừng hỗn giao."
    },
    "Sarcomyxa serotina": {
        "scientific_name": "Sarcomyxa serotina",
        "vn_name": "Nấm sò mùa đông (Late Fall Oyster)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Cần nấu kỹ)",
        "toxicity_level": "none",
        "description": "Mũ màu lục ô-liu pha vàng cam mọc vào cuối thu chớm đông, thịt dày, hơi có vị đắng nhẹ nếu nấu sơ.",
        "habitat": "Thân cây gỗ cứng mục vào mùa lạnh."
    },
    "Stropharia ambigua": {
        "scientific_name": "Stropharia ambigua",
        "vn_name": "Nấm mũ vàng viền ren trắng",
        "edibility": "caution",
        "edibility_vn": "Nghi ngờ / Cần thận trọng",
        "toxicity_level": "uncertain",
        "description": "Mũ nấm màu vàng tươi bắt mắt với dải vảy trắng như viền ren cotton viền quanh mép mũ.",
        "habitat": "Trên thảm mùn lá thông dày vùng Tây Bắc Mỹ."
    },
    "Suillus spraguei": {
        "scientific_name": "Suillus spraguei",
        "vn_name": "Nấm thông sơn vẽ (Painted Suillus)",
        "edibility": "edible",
        "edibility_vn": "Ăn được",
        "toxicity_level": "none",
        "description": "Mũ nấm xơ có các mảng vảy màu đỏ rượu vang trên nền vàng, cộng sinh chặt chẽ với cây thông trắng.",
        "habitat": "Chỉ mọc dưới tán cây thông trắng 5 lá (White Pine)."
    },
    "Tricholoma murrillianum": {
        "scientific_name": "Tricholoma murrillianum",
        "vn_name": "Nấm Matsutake miền Tây (Tùng nhung)",
        "edibility": "edible",
        "edibility_vn": "Ăn được (Cực kỳ quý hiếm & đắt đỏ)",
        "toxicity_level": "none",
        "description": "Loài nấm tùng nhung trứ danh với hương thơm quế và gia vị cay nồng đặc trưng, giá trị kinh tế rất cao.",
        "habitat": "Cộng sinh với cây thông và sồi trên núi cát cằn cỗi."
    }
}
