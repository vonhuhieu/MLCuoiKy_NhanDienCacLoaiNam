-- ==========================================================
-- HỆ CƠ SỞ DỮ LIỆU: NHẬN DIỆN CÁC LOÀI NẤM (MUSHROOM CLASSIFICATION)
-- Phục vụ cho: Spring Boot + MySQL + VueJS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `mushroom_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `mushroom_db`;

-- 1. BẢNG DANH MỤC 44 LOÀI NẤM (MUSHROOMS)
DROP TABLE IF EXISTS `mushrooms`;
CREATE TABLE `mushrooms` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `scientific_name` VARCHAR(100) NOT NULL UNIQUE COMMENT 'Tên khoa học (Khớp với nhãn model)',
    `vn_name` VARCHAR(150) NOT NULL COMMENT 'Tên tiếng Việt',
    `edibility` ENUM('edible', 'toxic', 'inedible', 'caution') NOT NULL COMMENT 'Mức độ ăn được/độc',
    `edibility_vn` VARCHAR(100) NOT NULL COMMENT 'Mô tả độc tính tiếng Việt',
    `toxicity_level` VARCHAR(50) DEFAULT 'none' COMMENT 'Cấp độ độc tính',
    `description` TEXT COMMENT 'Đặc điểm nhận diện',
    `habitat` TEXT COMMENT 'Môi trường sống',
    `image_url` VARCHAR(255) DEFAULT NULL COMMENT 'Đường dẫn ảnh mẫu đại diện',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. BẢNG LỊCH SỬ NHẬN DIỆN (PREDICTION_HISTORY)
DROP TABLE IF EXISTS `prediction_history`;
CREATE TABLE `prediction_history` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `image_path` VARCHAR(255) NOT NULL COMMENT 'Đường dẫn ảnh người dùng tải lên',
    `predicted_scientific_name` VARCHAR(100) NOT NULL COMMENT 'Tên loài dự đoán',
    `confidence` FLOAT NOT NULL COMMENT 'Độ tin cậy xác suất (%)',
    `model_used` VARCHAR(50) NOT NULL COMMENT 'ResNet50 / DenseNet121 / MobileNetV2',
    `top5_result_json` JSON COMMENT 'Toàn bộ top 5 kết quả dạng JSON',
    `feedback_status` VARCHAR(20) DEFAULT NULL COMMENT 'User feedback: correct / incorrect',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_predicted_name` (`predicted_scientific_name`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. NẠP DỮ LIỆU BAN ĐẦU CHO 44 LOÀI NẤM (SEED DATA)
INSERT INTO `mushrooms` (`scientific_name`, `vn_name`, `edibility`, `edibility_vn`, `toxicity_level`, `description`, `habitat`) VALUES
('Agaricus augustus', 'Nấm mỡ hoàng tử (The Prince)', 'edible', 'Ăn được (Ngon)', 'none', 'Nấm lớn, có mùi thơm như quả hạnh nhân hoặc hoa hồi, mũ nấm có vảy màu nâu vàng.', 'Thường mọc dưới các gốc thông hoặc ven đường rừng hỗn giao.'),
('Amanita amerirubescens', 'Nấm tán đỏ Mỹ (Blusher)', 'caution', 'Cần cẩn trọng (Phải nấu chín kỹ)', 'mild_when_raw', 'Thịt nấm chuyển sang màu ửng đỏ khi bị xước hoặc dập. Chứa độc tố tan máu khi ăn sống, chỉ an toàn khi nấu chín kỹ.', 'Mọc cộng sinh với cây sồi, thông trong rừng cây lá rộng.'),
('Amanita brunnescens', 'Nấm tán nâu hình sao', 'toxic', 'Có độc', 'moderate', 'Mũ nấm màu nâu xám, gốc củ có các vết nứt dọc đặc trưng dạng khe rãnh.', 'Mọc đơn lẻ hoặc thành cụm nhỏ trong rừng sồi, thông.'),
('Amanita calyptroderma', 'Nấm mũ áo choàng mỏng', 'edible', 'Ăn được (Rất ngon)', 'none', 'Mũ nấm màu vàng cam hoặc nâu vàng, thường mang một mảng bao chung lớn màu trắng ở đỉnh mũ.', 'Phổ biến ở bờ Tây Bắc Mỹ, mọc dưới tán sồi và cây lá kim.'),
('Amanita flavoconia', 'Nấm tán vảy vàng', 'toxic', 'Nghi ngờ có độc / Độc', 'moderate', 'Mũ nấm màu vàng tươi đến cam, phủ các đốm bột màu vàng lưu huỳnh.', 'Mọc trên đất rừng nhiều mùn, cộng sinh với cây lá kim và sồi.'),
('Amanita muscaria', 'Nấm tán bay / Nấm ruồi (Fly Agaric)', 'toxic', 'Độc (Gây ảo giác & rối loạn thần kinh)', 'high', 'Biểu tượng nấm kinh điển: Mũ đỏ tươi phủ vảy trắng đốm. Chứa acid ibotenic và muscimol gây ngộ độc thần kinh.', 'Rừng thông, rừng bạch dương vùng ôn đới.'),
('Amanita velosa', 'Nấm tán cam mùa xuân', 'edible', 'Ăn được (Hảo hạng)', 'none', 'Mũ màu hồng đào đến cam nhạt, mép khía rõ, không có vòng bao ở thân, gốc có bao chung dạng túi sâu.', 'Mọc vào mùa xuân dưới gốc sồi.'),
('Armillaria mellea', 'Nấm mật ong (Honey Mushroom)', 'edible', 'Ăn được (Nấu kỹ)', 'mild_when_raw', 'Mũ màu vàng mật ong, mọc thành chùm lớn quanh gốc cây mục. Ăn sống có thể gây khó chịu dạ dày.', 'Ký sinh và hoại sinh trên các thân gỗ mục, gốc cây.'),
('Armillaria tabescens', 'Nấm mật không vòng', 'edible', 'Ăn được', 'none', 'Tương tự nấm mật ong nhưng thân nấm không có vòng đệm (ringless). Mọc thành cụm rậm rạp.', 'Quanh gốc cây mục hoặc rễ cây ngầm.'),
('Artomyces pyxidatus', 'Nấm san hô hình vương miện', 'edible', 'Ăn được', 'none', 'Hình dáng như nhánh san hô phân nhánh, đầu mỗi nhánh hình cái chén nhỏ như vương miện.', 'Mọc trực tiếp trên các khúc gỗ mục ẩm ướt trong rừng.'),
('Bolbitius titubans', 'Nấm mũ vàng nhầy', 'inedible', 'Không ăn được (Thịt mỏng)', 'none', 'Mũ nấm màu vàng sáng lúc non, sau chuyển sang xám nhạt có khía, bề mặt nhớt nhầy, thịt rất mỏng manh.', 'Mọc trên phân mục hoặc bãi cỏ ẩm giàu dinh dưỡng.'),
('Boletus pallidus', 'Nấm gan bò nhợt', 'edible', 'Ăn được', 'none', 'Mũ màu xám trắng đến vàng nhạt, lớp lỗ xốp dưới mũ ngả xanh lam khi bị cọ xát hoặc cắt.', 'Mọc dưới cây sồi và rừng hỗn giao.'),
('Boletus rex-veris', 'Nấm vua mùa xuân (Spring King Bolete)', 'edible', 'Ăn được (Hảo hạng)', 'none', 'Nấm lớn, thịt dày chắc, mũ nâu đỏ bóng, vị ngọt bùi giá trị ẩm thực rất cao.', 'Mọc ven rừng lá kim trên núi cao vào mùa xuân.'),
('Cantharellus californicus', 'Nấm mồng gà khổng lồ California', 'edible', 'Ăn được (Hảo hạng)', 'none', 'Có hình phễu màu vàng mơ, thịt dày thơm mùi quả đào/mơ, là loài nấm mồng gà lớn nhất thế giới.', 'Cộng sinh với cây sồi ven bờ biển California.'),
('Cantharellus cinnabarinus', 'Nấm mồng gà đỏ chu sa', 'edible', 'Ăn được', 'none', 'Kích thước nhỏ nhắn, nổi bật với màu đỏ hồng đến đỏ cam rực rỡ như chu sa.', 'Mọc trên nền rừng sồi và rừng rụng lá.'),
('Cerioporus squamosus', 'Nấm yên ngựa gỗ (Dryad''s Saddle)', 'edible', 'Ăn được (Khi còn non)', 'none', 'Hình dáng quạt lớn xòe ngang thân cây gỗ, mặt trên có vảy nâu sẫm, khi non có mùi dưa chuột mát.', 'Mọc trên thân cây gỗ rụng lá mục hoặc sống.'),
('Clitocybe nuda', 'Nấm hương tím (Wood Blewit)', 'edible', 'Ăn được (Nấu chín)', 'mild_when_raw', 'Mũ và phiến nấm có màu tím hoa cà rất đẹp, hương thơm nhẹ, ăn sống dễ gây dị ứng tiêu hóa.', 'Mọc trên lớp thảm lá mục hoặc đống phân ủ mục nát.'),
('Coprinellus micaceus', 'Nấm mực vảy óng ánh', 'edible', 'Ăn được (Nấu ngay)', 'none', 'Mũ nấm hình chuông màu nâu nhạt, phủ các hạt lấp lánh như vảy mica, tự chảy rữa thành mực đen khi già.', 'Mọc thành cụm quanh gốc cây mục mục ruỗng.'),
('Coprinus comatus', 'Nấm mực lông gà (Shaggy Mane)', 'edible', 'Ăn được (Ngon khi non)', 'none', 'Mũ thon dài phủ vảy xù xì màu trắng, thịt mềm ngọt nhưng phải chế biến ngay trước khi nấm tự hóa lỏng thành mực.', 'Bãi cỏ, ven đường, công viên đất mùn ẩm.'),
('Daedaleopsis confragosa', 'Nấm vân gỗ mê lộ', 'inedible', 'Không ăn được (Thớ gỗ cứng dai)', 'none', 'Nấm dạng dĩa bám thân gỗ, mặt dưới lỗ xếp như hình mê cung, thể quả hóa gỗ cứng dai.', 'Mọc trên các cành bạch dương, liễu mục.'),
('Entoloma abortivum', 'Nấm thợ săn tôm non (Shrimp Mushroom)', 'edible', 'Ăn được (Ngon)', 'none', 'Thường gặp ở dạng biến dạng màu trắng xốp như viên bỏng ngô do ký sinh lên nấm mật ong, vị giòn ngọt.', 'Rừng lá rộng nhiều cây mục ẩm ướt.'),
('Flammulina velutipes', 'Nấm kim châm hoang dã', 'edible', 'Ăn được (Rất phổ biến)', 'none', 'Dạng hoang dã có mũ màu vàng nâu nhớt, chân nhung đen sẫm, khác với dạng nấm kim châm trắng nuột nuôi cấy.', 'Mọc trên thân cây gỗ mục mùa lạnh.'),
('Ganoderma applanatum', 'Nấm linh chi tán phẳng / Nấm bảng vẽ họa sĩ', 'inedible', 'Không ăn được (Dược liệu/Nghệ thuật)', 'none', 'Thể quả gỗ cứng như đá xòe quạt to, mặt dưới trắng mịn cào vẽ được tranh, dùng sắc thuốc uống.', 'Ký sinh sống dai nhiều năm trên thân gỗ già.'),
('Grifola frondosa', 'Nấm khiêu vũ / Nấm Maitake', 'edible', 'Ăn được & Dược liệu quý', 'none', 'Cụm nấm lớn gồm hàng trăm mũ nhỏ màu nâu xám xòe lớp lang như váy múa, tăng cường miễn dịch.', 'Dưới gốc cây sồi cổ thụ.'),
('Hericium coralloides', 'Nấm hầu thủ san hô', 'edible', 'Ăn được (Hảo hạng)', 'none', 'Hình dáng tuyệt đẹp như san hô trắng tinh khiết rủ các sợi gai nhọn, thịt thơm ngọt thanh.', 'Mọc trên các thân gỗ phong, sồi mục rụng.'),
('Hygrophoropsis aurantiaca', 'Nấm mồng gà giả (False Chanterelle)', 'caution', 'Cần thận trọng (Có thể đau bụng)', 'mild', 'Dễ nhầm với nấm mồng gà ăn được nhưng phiến mỏng rẽ đôi và mũ màu cam rực rỡ hơn.', 'Rừng cây lá kim trên lớp mùn thông mục.'),
('Hypholoma fasciculare', 'Nấm đầu lưu huỳnh (Sulfur Tuft)', 'toxic', 'ĐỘC NGUY HIỂM', 'high', 'Mọc thành chùm lớn màu vàng lưu huỳnh rực rỡ, vị rất đắng. Chứa fasciculol gây nôn ói và tổn thương gan.', 'Mọc dày đặc trên gốc và thân gỗ mục rữa.'),
('Hypomyces lactifluorum', 'Nấm tôm hùm (Lobster Mushroom)', 'edible', 'Ăn được (Đặc sản quý)', 'none', 'Nấm ký sinh phủ lớp vỏ ngoài màu đỏ cam như mai tôm hùm luộc chín, vị giòn ngọt hương hải sản.', 'Ký sinh lên nấm Russula hoặc Lactarius trong rừng thông.'),
('Ischnoderma resinosum', 'Nấm da gỉ nhựa', 'edible', 'Ăn được khi non', 'none', 'Khi còn non tiết ra các giọt chất lỏng màu hổ phách ở mép nấm, thịt mềm có thể chế biến như thịt bò.', 'Thân gỗ cứng mục rụng.'),
('Laetiporus sulphureus', 'Nấm gà rừng (Chicken of the Woods)', 'edible', 'Ăn được (Thơm ngon như thịt gà)', 'none', 'Xòe nhiều tầng màu vàng cam rực rỡ, xào nướng vị xé thớ như ức gà. Lưu ý một số người dị ứng nhẹ.', 'Mọc trên thân cây sồi già hoặc cây gỗ lá rộng.'),
('Lycoperdon perlatum', 'Nấm trứng ngọc trai (Gem-studded Puffball)', 'edible', 'Ăn được khi ruột còn trắng tinh', 'none', 'Thân hình con quay tròn phủ gai hạt ngọc, ăn được khi bên trong trắng mịn như đậu phụ.', 'Đất rừng, ven đường mòn ẩm.'),
('Lycoperdon pyriforme', 'Nấm trứng hình quả lê', 'edible', 'Ăn được khi còn non', 'none', 'Hình dáng giống quả lê nhỏ, mọc thành bầy dày đặc trên thân gỗ mục.', 'Trên các khúc gỗ mục rữa trong rừng ẩm.'),
('Mycena haematopus', 'Nấm tiên mũ máu (Bleeding Fairy Helmet)', 'inedible', 'Không ăn được', 'none', 'Nấm nhỏ thanh mảnh, khi thân bị gãy sẽ ứa ra giọt dịch màu đỏ thẫm như máu.', 'Mọc trên cành mục ẩm ướt.'),
('Omphalotus illudens', 'Nấm đèn lồng ma (Jack-o''-Lantern)', 'toxic', 'ĐỘC (Gây ảo giác & đau bụng nặng)', 'high', 'Màu cam rực rỡ, phiến nấm phát quang sinh học màu lục trong bóng tối. Rất dễ nhầm với nấm mồng gà.', 'Gốc cây sồi mục thành từng cụm lớn.'),
('Omphalotus olivascens', 'Nấm đèn lồng ô-liu bờ Tây', 'toxic', 'ĐỘC', 'high', 'Tương tự nấm đèn lồng ma nhưng có sắc xanh lục ô-liu pha cam, chứa độc tố illudin gây buồn nôn, co thắt dạ dày.', 'Mọc quanh gốc cây sồi và bạch đàn ở California.'),
('Phlebia tremellosa', 'Nấm màng nhăn thạch', 'inedible', 'Không ăn được', 'none', 'Trải dẹt như tấm thạch nhăn nheo bám mặt gỗ, màu cam hồng nhạt, chất thạch dai keo.', 'Mặt dưới cành cây mục rụng.'),
('Pleurotus ostreatus', 'Nấm sò / Nấm bào ngư xám', 'edible', 'Ăn được (Ngon & phổ biến)', 'none', 'Mũ hình vỏ sò màu xám tro, thớ thịt ngọt dai giòn, được nuôi trồng và tiêu thụ rộng rãi.', 'Mọc trên thân cây gỗ mục khắp nơi.'),
('Pleurotus pulmonarius', 'Nấm sò phượng hoàng / Sò trắng', 'edible', 'Ăn được', 'none', 'Tương tự nấm sò xám nhưng mũ mỏng hơn và có màu trắng ngà hoặc xám nhạt, ưa mùa hè.', 'Mọc trên thân cây gỗ lá rộng vào mùa ấm áp.'),
('Psilocybe pelliculosa', 'Nấm thần tiên / Nấm thức thần màng nhầy', 'toxic', 'ĐỘC / THỨC THẦN (Chất cấm gây ảo giác)', 'hallucinogenic', 'Mũ nấm hình chuông nhỏ màu nâu caramen, chứa psilocybin gây ảo giác thị giác và thay đổi tâm thần.', 'Ven đường mòn phủ mùn cưa và rêu trong rừng cây lá kim.'),
('Retiboletus ornatipes', 'Nấm gan bò chân ren vàng', 'inedible', 'Không ăn được (Vị đắng chát)', 'none', 'Chân nấm có hoa văn vân lưới dập nổi màu vàng chanh rất đẹp nhưng thịt nấm cực kỳ đắng.', 'Rừng sồi và rừng hỗn giao.'),
('Sarcomyxa serotina', 'Nấm sò mùa đông (Late Fall Oyster)', 'edible', 'Ăn được (Cần nấu kỹ)', 'none', 'Mũ màu lục ô-liu pha vàng cam mọc vào cuối thu chớm đông, thịt dày, hơi có vị đắng nhẹ nếu nấu sơ.', 'Thân cây gỗ cứng mục vào mùa lạnh.'),
('Stropharia ambigua', 'Nấm mũ vàng viền ren trắng', 'caution', 'Nghi ngờ / Cần thận trọng', 'uncertain', 'Mũ nấm màu vàng tươi bắt mắt với dải vảy trắng như viền ren cotton viền quanh mép mũ.', 'Trên thảm mùn lá thông dày vùng Tây Bắc Mỹ.'),
('Suillus spraguei', 'Nấm thông sơn vẽ (Painted Suillus)', 'edible', 'Ăn được', 'none', 'Mũ nấm xơ có các mảng vảy màu đỏ rượu vang trên nền vàng, cộng sinh chặt chẽ với cây thông trắng.', 'Chỉ mọc dưới tán cây thông trắng 5 lá (White Pine).'),
('Tricholoma murrillianum', 'Nấm Matsutake miền Tây (Tùng nhung)', 'edible', 'Ăn được (Cực kỳ quý hiếm & đắt đỏ)', 'none', 'Loài nấm tùng nhung trứ danh với hương thơm quế và gia vị cay nồng đặc trưng, giá trị kinh tế rất cao.', 'Cộng sinh với cây thông và sồi trên núi cát cằn cỗi.');

