#!/usr/bin/env python3
"""Build vocabulary markdown files from IELTS Fighter lessons and Simon source."""

import os
import re
import fitz
from collections import defaultdict

BASE = "/Users/ngocdunghuynh/githubs/ielts/SPEAKING "
VOCAB_DIR = os.path.join(BASE, "vocabulary")

Entry = dict  # keys: english, cefr, phonetics, vietnamese


def md_table(rows: list[Entry], headers=("English", "CEFR", "Phonetics", "Vietnamese")) -> list[str]:
    lines = [
        f"| {headers[0]} | {headers[1]} | {headers[2]} | {headers[3]} |",
        "|---------|------|-----------|------------|",
    ]
    for r in rows:
        lines.append(f"| {r.get('english','')} | {r.get('cefr','')} | {r.get('phonetics','')} | {r.get('vietnamese','')} |")
    return lines


def md_phrases(phrases: list[str]) -> list[str]:
    return [f"- {p}" for p in phrases]


def write_lesson(slug: str, title: str, source: str, vocab=None, coll=None, phrases=None, extra=""):
    lines = [
        f"# {title}",
        "",
        f"> Source: `{source}`",
        f"> File: `{slug}.md`",
        "",
    ]
    if extra:
        lines += [extra, ""]
    if vocab:
        lines += ["## Vocabulary", ""] + md_table(vocab) + [""]
    if coll:
        lines += ["## Collocations", ""] + md_table(coll) + [""]
    if phrases:
        lines += ["## Useful Expressions / Phrases", ""] + md_phrases(phrases) + [""]
    path = os.path.join(VOCAB_DIR, f"{slug}.md")
    with open(path, "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    return len(vocab or []), len(coll or []), len(phrases or [])


# ─── LESSON 1 ───────────────────────────────────────────────────────────────
L1_VOCAB = [
    {"english": "haircut (n)", "cefr": "B1", "phonetics": "/ˈherkʌt/", "vietnamese": "Sự cắt tóc, kiểu tóc"},
    {"english": "dye (v)", "cefr": "B2", "phonetics": "/daɪ/", "vietnamese": "Nhuộm"},
    {"english": "gifted (adj)", "cefr": "C1", "phonetics": "/ˈɡɪftɪd/", "vietnamese": "Có năng khiếu, có tài"},
    {"english": "inherit (v)", "cefr": "B2", "phonetics": "/ɪnˈherɪt/", "vietnamese": "Thừa hưởng, kế thừa"},
    {"english": "innate (adj)", "cefr": "C2", "phonetics": "/ɪˈneɪt/", "vietnamese": "Bẩm sinh"},
    {"english": "nickname (n)", "cefr": "B1", "phonetics": "/ˈnɪkneɪm/", "vietnamese": "Biệt danh"},
    {"english": "name (v)", "cefr": "A1", "phonetics": "/neɪm/", "vietnamese": "Đặt tên"},
    {"english": "imply (v)", "cefr": "B2", "phonetics": "/ɪmˈplaɪ/", "vietnamese": "Ngụ ý"},
    {"english": "aspiration (n)", "cefr": "C1", "phonetics": "/ˌæspəˈreɪʃn/", "vietnamese": "Khát vọng"},
    {"english": "amnesia (n)", "cefr": "C2", "phonetics": "/æmˈniːʒə/", "vietnamese": "Chứng lẫn, chứng quên"},
    {"english": "recall (v)", "cefr": "B1", "phonetics": "/rɪˈkɔːl/", "vietnamese": "Nhớ lại"},
    {"english": "reminisce (v)", "cefr": "C1", "phonetics": "/ˌremɪˈnɪs/", "vietnamese": "Hồi tưởng lại"},
    {"english": "ambience (n)", "cefr": "NA", "phonetics": "/ˈæmbiəns/", "vietnamese": "Không khí, môi trường xung quanh"},
    {"english": "disturb (v)", "cefr": "B2", "phonetics": "/dɪˈstɜːrb/", "vietnamese": "Gây ồn ào, náo động"},
    {"english": "procrastinator (n)", "cefr": "NA", "phonetics": "/prəˈkræstəˌneɪtər/", "vietnamese": "Người trì hoãn"},
    {"english": "get distracted", "cefr": "B2", "phonetics": "/ɡɛt dɪˈstræktɪd/", "vietnamese": "Bị phân tâm"},
    {"english": "well-known (adj)", "cefr": "B1", "phonetics": "/ˌwel ˈnəʊn/", "vietnamese": "Nổi tiếng về"},
    {"english": "trendsetter (n)", "cefr": "B2", "phonetics": "/ˈtrendsetər/", "vietnamese": "Người dẫn đầu xu hướng"},
    {"english": "desire (n/v)", "cefr": "B2", "phonetics": "/dɪˈzaɪər/", "vietnamese": "Khao khát, mong muốn"},
    {"english": "fulfill (v)", "cefr": "B2", "phonetics": "/fʊlˈfɪl/", "vietnamese": "Hoàn thành, làm tròn"},
    {"english": "repetitive (adj)", "cefr": "B2", "phonetics": "/rɪˈpetətɪv/", "vietnamese": "Lặp đi lặp lại"},
    {"english": "meaningful (adj)", "cefr": "C1", "phonetics": "/ˈmiːnɪŋfl/", "vietnamese": "Có ý nghĩa"},
    {"english": "contentment (n)", "cefr": "NA", "phonetics": "/kənˈtentmənt/", "vietnamese": "Sự hài lòng"},
    {"english": "morale (n)", "cefr": "C2", "phonetics": "/məˈræl/", "vietnamese": "Tinh thần"},
    {"english": "anticipation (n)", "cefr": "B2", "phonetics": "/ænˌtɪsɪˈpeɪʃn/", "vietnamese": "Sự hào hứng, mong chờ"},
    {"english": "purchase (v)", "cefr": "B2", "phonetics": "/ˈpɜːrtʃəs/", "vietnamese": "Mua thứ gì đó"},
    {"english": "magical time (n)", "cefr": "C1", "phonetics": "/ˈmædʒɪkl taɪm/", "vietnamese": "Quãng thời gian kì diệu"},
    {"english": "mundane matters (n)", "cefr": "C1", "phonetics": "/mʌnˈdeɪn ˈmætərz/", "vietnamese": "Những công việc hàng ngày"},
    {"english": "tedious (adj)", "cefr": "C1", "phonetics": "/ˈtiːdiəs/", "vietnamese": "Tẻ nhạt"},
    {"english": "monotonous (adj)", "cefr": "C1", "phonetics": "/məˈnɑːtənəs/", "vietnamese": "Đơn điệu"},
    {"english": "boredom (n)", "cefr": "B2", "phonetics": "/ˈbɔːrdəm/", "vietnamese": "Sự buồn tẻ, buồn chán"},
]
L1_COLL = [
    {"english": "ruin one's hair", "cefr": "B2", "phonetics": "/ˈruːɪn wʌnz her/", "vietnamese": "Làm hỏng tóc của ai đó"},
    {"english": "cut something way too short", "cefr": "B1", "phonetics": "/kʌt ˈsʌmθɪŋ weɪ tu ʃɔrt/", "vietnamese": "Cắt cái gì đó quá ngắn"},
    {"english": "turn out a lot better", "cefr": "B2", "phonetics": "/tɜrn aʊt ə lɑt ˈbɛtər/", "vietnamese": "Hóa ra tốt hơn rất nhiều"},
    {"english": "long scuffy hair", "cefr": "B2", "phonetics": "/lɔŋ ˈskrʌfi her/", "vietnamese": "Tóc dài rối bù"},
    {"english": "get a haircut", "cefr": "B1", "phonetics": "/ɡɛt ə ˈhɛrˌkʌt/", "vietnamese": "Cắt tóc"},
    {"english": "dye one's hair", "cefr": "B2", "phonetics": "/daɪ wʌnz her/", "vietnamese": "Nhuộm tóc ai đó"},
    {"english": "hone one's skill", "cefr": "B1", "phonetics": "/hoʊn wʌnz skɪl/", "vietnamese": "Trau dồi kỹ năng của ai đó"},
    {"english": "a natural at something", "cefr": "B1", "phonetics": "/ə ˈnætʃrəl æt ˈsʌmθɪŋ/", "vietnamese": "Có năng khiếu tự nhiên về một điều gì"},
    {"english": "mess someone's name up", "cefr": "B2", "phonetics": "/mɛs ˈsʌmˌwʌnz neɪm ʌp/", "vietnamese": "Đọc sai tên ai đó"},
    {"english": "a competitive spirit", "cefr": "B1", "phonetics": "/ə kəmˈpetətɪv ˈspɪrɪt/", "vietnamese": "Tinh thần cạnh tranh"},
    {"english": "stick in one's mind", "cefr": "B2", "phonetics": "/stɪk ɪn wʌnz maɪnd/", "vietnamese": "Gắn trong tâm trí ai đó"},
    {"english": "immerse oneself in", "cefr": "C1", "phonetics": "/ɪˈmɜːrs wʌnˈsɛlf ɪn/", "vietnamese": "Đắm chìm vào việc gì đó"},
    {"english": "show off one's status", "cefr": "B2", "phonetics": "/ʃoʊ ɔf wʌnz ˈsteɪtəs/", "vietnamese": "Khoe mẽ địa vị của ai đó"},
    {"english": "make one's day", "cefr": "C2", "phonetics": "/meɪk wʌnz deɪ/", "vietnamese": "Làm ngày của ai đó cảm thấy vui vẻ"},
    {"english": "bring someone immense joy", "cefr": "C1", "phonetics": "/brɪŋ ˈsʌmˌwʌn ɪˈmɛns ʤɔɪ/", "vietnamese": "Mang cho ai đó niềm vui to lớn"},
    {"english": "retail therapy", "cefr": "C1", "phonetics": "/ˈriːteɪl ˌθerəpi/", "vietnamese": "Trị liệu mua sắm"},
    {"english": "get on someone's nerves", "cefr": "B2", "phonetics": "/ɡɛt ɑn ˈsʌmˌwʌnz nɜrvz/", "vietnamese": "Làm ai đó bực mình"},
    {"english": "bored to death/tears", "cefr": "C1", "phonetics": "/bɔrd tu dɛθ/ /tɛrz/", "vietnamese": "Chán chết, cực kì buồn chán"},
]

# ─── LESSON 2 ───────────────────────────────────────────────────────────────
L2_VOCAB = [
    {"english": "notification (n)", "cefr": "B2", "phonetics": "/ˌnəʊtɪfɪˈkeɪʃn/", "vietnamese": "Thông báo"},
    {"english": "platform (n)", "cefr": "C2", "phonetics": "/ˈplætfɔːrm/", "vietnamese": "Nền tảng"},
    {"english": "delusion (n)", "cefr": "NA", "phonetics": "/dɪˈluːʒn/", "vietnamese": "Ảo tưởng"},
    {"english": "scam (n)", "cefr": "C1", "phonetics": "/skæm/", "vietnamese": "Trò lừa đảo"},
    {"english": "medium (n)", "cefr": "B2", "phonetics": "/ˈmiːdiəm/", "vietnamese": "Phương tiện"},
    {"english": "binge watching (n)", "cefr": "NA", "phonetics": "/ˈbɪndʒ wɑːtʃɪŋ/", "vietnamese": "Cày phim"},
    {"english": "interface (n)", "cefr": "C1", "phonetics": "/ˈɪntərfeɪs/", "vietnamese": "Giao diện"},
    {"english": "layout (n)", "cefr": "C1", "phonetics": "/ˈleɪaʊt/", "vietnamese": "Bố cục"},
    {"english": "crash (n/v)", "cefr": "B2", "phonetics": "/kræʃ/", "vietnamese": "Bị hư (máy tính)"},
    {"english": "sedentary (adj)", "cefr": "C2", "phonetics": "/ˈsednteri/", "vietnamese": "Ngồi nhiều (ít vận động)"},
    {"english": "sensational (adj)", "cefr": "C1", "phonetics": "/senˈseɪʃənl/", "vietnamese": "Giật gân"},
    {"english": "ubiquitous (adj)", "cefr": "NA", "phonetics": "/juːˈbɪkwɪtəs/", "vietnamese": "Phổ biến"},
    {"english": "impulsive (adj)", "cefr": "C2", "phonetics": "/ɪmˈpʌlsɪv/", "vietnamese": "Bốc đồng"},
    {"english": "work-related (adj)", "cefr": "NA", "phonetics": "/ˈwɜːkrɪleɪtɪd/", "vietnamese": "Có liên quan tới công việc"},
    {"english": "handy (adj)", "cefr": "C1", "phonetics": "/ˈhændi/", "vietnamese": "Tiện lợi"},
    {"english": "computer-literate (adj)", "cefr": "C1", "phonetics": "/kəmˌpjuːtər ˈlɪtərət/", "vietnamese": "Am hiểu về máy tính"},
    {"english": "short-sighted (adj)", "cefr": "B2", "phonetics": "/ˌʃɔːrt ˈsaɪtɪd/", "vietnamese": "Cận thị"},
    {"english": "graphic (adj)", "cefr": "B2", "phonetics": "/ˈɡræfɪk/", "vietnamese": "Đồ họa"},
    {"english": "portable (adj)", "cefr": "C1", "phonetics": "/ˈpɔːrtəbl/", "vietnamese": "Có thể mang theo, di động"},
    {"english": "on-going (adj)", "cefr": "B2", "phonetics": "/ˈɑːnɡəʊɪŋ/", "vietnamese": "Đang tiếp diễn"},
    {"english": "endorse (v)", "cefr": "C1", "phonetics": "/ɪnˈdɔːrs/", "vietnamese": "Đóng quảng cáo (người nổi tiếng)"},
    {"english": "tout (v)", "cefr": "NA", "phonetics": "/taʊt/", "vietnamese": "Chào hàng"},
    {"english": "exaggerate (v)", "cefr": "C1", "phonetics": "/ɪɡˈzædʒəreɪt/", "vietnamese": "Thổi phồng"},
    {"english": "compose (v)", "cefr": "B2", "phonetics": "/kəmˈpoʊz/", "vietnamese": "Soạn"},
    {"english": "fulfill (v)", "cefr": "B2", "phonetics": "/fʊlˈfɪl/", "vietnamese": "Làm trọn vẹn, đáp ứng"},
    {"english": "enroll (v)", "cefr": "C1", "phonetics": "/ɪnˈroʊl/", "vietnamese": "Trở thành thành viên của, kết nạp"},
    {"english": "snap (v)", "cefr": "C1", "phonetics": "/snæp/", "vietnamese": "Chụp nhanh"},
    {"english": "navigate (v)", "cefr": "B2", "phonetics": "/ˈnævɪɡeɪt/", "vietnamese": "Tìm đường"},
    {"english": "retouch (v)", "cefr": "NA", "phonetics": "/ˌriːˈtʌtʃ/", "vietnamese": "Chỉnh sửa (ảnh)"},
    {"english": "via (adv)", "cefr": "B2", "phonetics": "/ˈvaɪə/", "vietnamese": "Thông qua"},
    {"english": "hassle (n)", "cefr": "B2", "phonetics": "/ˈhæsl/", "vietnamese": "Điều rắc rối phức tạp"},
    {"english": "intensity (n)", "cefr": "C1", "phonetics": "/ɪnˈtensəti/", "vietnamese": "Sự nghiêm trọng"},
    {"english": "congestion (n)", "cefr": "C1", "phonetics": "/kənˈdʒestʃən/", "vietnamese": "Tắc nghẽn (giao thông)"},
    {"english": "means (n)", "cefr": "B2", "phonetics": "/miːnz/", "vietnamese": "Phương tiện"},
    {"english": "flexibility (n)", "cefr": "B1", "phonetics": "/ˌfleksəˈbɪləti/", "vietnamese": "Tính linh hoạt"},
    {"english": "ease (v)", "cefr": "C1", "phonetics": "/iːz/", "vietnamese": "Làm giảm đi, dịu đi"},
    {"english": "fuel-efficient (adj)", "cefr": "NA", "phonetics": "/fjuːəl ɪˈfɪʃənt/", "vietnamese": "Tiết kiệm nhiên liệu"},
    {"english": "mindful (adj)", "cefr": "NA", "phonetics": "/ˈmaɪndfl/", "vietnamese": "Quan tâm, lưu tâm"},
    {"english": "herculean (adj)", "cefr": "NA", "phonetics": "/ˌhɜːrkjuˈliːən/", "vietnamese": "Khó khăn"},
    {"english": "mesmerizing (adj)", "cefr": "NA", "phonetics": "/ˈmezməraɪzɪŋ/", "vietnamese": "Mê hoặc"},
]
L2_COLL = [
    {"english": "keep abreast of the news", "cefr": "C1", "phonetics": "/kip əˈbrɛst ʌv ðə nuz/", "vietnamese": "Bám sát tin tức"},
    {"english": "get on one's nerves", "cefr": "B2", "phonetics": "/ɡɛt ɑn maɪnɜrvz/", "vietnamese": "Làm ai đó bực mình"},
    {"english": "delusion life", "cefr": "A1", "phonetics": "/dɪˈluʒən laɪf/", "vietnamese": "Cuộc sống ảo"},
    {"english": "targeted audience", "cefr": "A2", "phonetics": "/ˈtɑrɡətɪd ˈɑdiəns/", "vietnamese": "Người xem mục tiêu"},
    {"english": "take over the throne", "cefr": "B2", "phonetics": "/teɪk ˈoʊvər ðə θroʊn/", "vietnamese": "Chiếm ngai vàng (vị trí ưu thế)"},
    {"english": "meet entertainment needs", "cefr": "B2", "phonetics": "/mit ˌɛntərˈteɪnmənt nidz/", "vietnamese": "Đáp ứng nhu cầu giải trí"},
    {"english": "at one's own pace", "cefr": "B2", "phonetics": "/æt wʌnz oʊn peɪs/", "vietnamese": "Tùy thích / ở tốc độ của bản thân"},
    {"english": "catch sight of", "cefr": "B2", "phonetics": "/kæʧ saɪt ʌv/", "vietnamese": "Bắt gặp"},
    {"english": "be drawn to", "cefr": "B2", "phonetics": "/bi drɔn tu/", "vietnamese": "Bị thu hút bởi"},
    {"english": "impulsive decision", "cefr": "C1", "phonetics": "/ɪmˈpʌlsɪv dɪˈsɪʒən/", "vietnamese": "Quyết định bốc đồng"},
    {"english": "communication medium", "cefr": "B2", "phonetics": "/kəmˌjunəˈkeɪʃən ˈmidiəm/", "vietnamese": "Phương tiện giao tiếp"},
    {"english": "work-related email", "cefr": "A1", "phonetics": "/wɜrk-rɪˈleɪtɪd iˈmeɪl/", "vietnamese": "Thư điện tử liên quan đến công việc"},
    {"english": "workplace communication", "cefr": "B1", "phonetics": "/ˈwɜrkˌpleɪs kəmˌjunəˈkeɪʃən/", "vietnamese": "Sự giao tiếp nơi công sở"},
    {"english": "messaging platform", "cefr": "B2", "phonetics": "/ˈmɛsɪʤɪŋ ˈplætˌfɔrm/", "vietnamese": "Nền tảng tin nhắn"},
    {"english": "online movie streaming platform", "cefr": "B2", "phonetics": "/ˈɔnˌlaɪn ˈmuvi ˈstrimɪŋ ˈplætˌfɔrm/", "vietnamese": "Nền tảng xem phim trực tuyến"},
    {"english": "come in handy", "cefr": "B2", "phonetics": "/kʌm ɪn ˈhændi/", "vietnamese": "Tiện lợi"},
    {"english": "can't go a day without", "cefr": "B1", "phonetics": "/kænt ɡoʊ ə deɪ wɪˈθaʊt/", "vietnamese": "Không thể sống nếu thiếu cái gì"},
    {"english": "have a heavy influence on", "cefr": "B2", "phonetics": "/hæv ə ˈhɛvi ˈɪnfluəns ɑn/", "vietnamese": "Có ảnh hưởng lớn tới"},
    {"english": "historical records", "cefr": "B1", "phonetics": "/hɪˈstɔrɪkəl rəˈkɔrdz/", "vietnamese": "Thước phim lịch sử"},
    {"english": "broaden one's horizon", "cefr": "B2", "phonetics": "/ˈbrɔdən wʌnz həˈraɪzən/", "vietnamese": "Mở rộng tầm nhìn"},
    {"english": "graphic design", "cefr": "B2", "phonetics": "/ˈɡræfɪk dɪˈzaɪn/", "vietnamese": "Thiết kế đồ họa"},
    {"english": "fulfill one's needs", "cefr": "B2", "phonetics": "/fʊlˈfɪl wʌnz nidz/", "vietnamese": "Đáp ứng nhu cầu"},
    {"english": "snap photos", "cefr": "C1", "phonetics": "/snæp ˈfoʊˌtoʊz/", "vietnamese": "Chụp ảnh"},
    {"english": "navigate one's way around", "cefr": "B2", "phonetics": "/ˈnævəˌɡeɪt wʌnz weɪ əˈraʊnd/", "vietnamese": "Tìm đường đi"},
    {"english": "mass transit", "cefr": "B2", "phonetics": "/mæs ˈtrænzɪt/", "vietnamese": "Phương tiện giao thông công cộng"},
    {"english": "save someone from the hassle of", "cefr": "B2", "phonetics": "/seɪv ˈsʌmˌwʌn frʌm ðə ˈhæsəl ʌv/", "vietnamese": "Giúp thoát khỏi sự phiền hà"},
    {"english": "ease the intensity of", "cefr": "C1", "phonetics": "/iz ði ɪnˈtɛnsəti ʌv/", "vietnamese": "Làm giảm sự nghiêm trọng của"},
    {"english": "traffic congestion", "cefr": "B1", "phonetics": "/ˈtræfɪk kənˈdʒɛsʧən/", "vietnamese": "Tắc nghẽn giao thông"},
    {"english": "carbon footprint", "cefr": "B2", "phonetics": "/ˈkɑrbən ˈfʊtˌprɪnt/", "vietnamese": "Khí thải carbon"},
    {"english": "a herculean task", "cefr": "A2", "phonetics": "/ə hərˈkjuliən tæsk/", "vietnamese": "Một việc / nhiệm vụ khó khăn"},
]
L2_PHRASES = [
    "**EPACT technique:** Example → Popularity → Advantage → Cost → Time",
]

# ─── LESSON 4 ───────────────────────────────────────────────────────────────
L4_COLL = [
    {"english": "one-of-a-kind", "cefr": "B2", "phonetics": "/wʌn-ʌv-ə-kaɪnd/", "vietnamese": "Độc nhất vô nhị"},
    {"english": "a panoramic view of", "cefr": "C1", "phonetics": "/ə ˌpænəˈræmɪk vju ʌv/", "vietnamese": "Tầm nhìn toàn cảnh"},
    {"english": "once in a lifetime experience", "cefr": "B2", "phonetics": "/wʌns ɪn ə ˈlaɪfˌtaɪm ɪkˈspɪriəns/", "vietnamese": "Trải nghiệm một lần trong đời"},
    {"english": "a genuine foodie", "cefr": "B2", "phonetics": "/ə ˈdʒenjuɪn ˈfuːdi/", "vietnamese": "Một người sành ăn thực sự"},
    {"english": "in the proximity to", "cefr": "C1", "phonetics": "/ɪn ðə prɑːkˈsɪməti tuː/", "vietnamese": "Gần với"},
    {"english": "delectable cuisines", "cefr": "C2", "phonetics": "/dɪˈlɛktəbəl kwɪˈzinz/", "vietnamese": "Ẩm thực ngon miệng"},
    {"english": "a sleepy place", "cefr": "B2", "phonetics": "/ə ˈslipi pleɪs/", "vietnamese": "Một nơi yên tĩnh"},
    {"english": "satisfy one's craving for", "cefr": "B2", "phonetics": "/ˈsætɪsfaɪ wʌnz ˈkreɪvɪŋ fɔr/", "vietnamese": "Thỏa mãn cơn thèm của ai"},
    {"english": "snag a table", "cefr": "B2", "phonetics": "/snæɡ ə ˈteɪbəl/", "vietnamese": "Chiếm được bàn"},
    {"english": "to die for", "cefr": "B2", "phonetics": "/tu daɪ fɔr/", "vietnamese": "Cực kỳ ngon / tuyệt vời"},
    {"english": "packed like sardines", "cefr": "C1", "phonetics": "/bi pækt laɪk sɑrˈdinz/", "vietnamese": "Đông nghẹt như cá hộp"},
    {"english": "first come, first served", "cefr": "B1", "phonetics": "/fɜrst kʌm, fɜrst sɜrvd/", "vietnamese": "Ai đến trước được phục vụ trước"},
    {"english": "serve as a reminder of", "cefr": "B2", "phonetics": "/sɜrv æz ə riˈmaɪndər ʌv/", "vietnamese": "Như lời nhắc nhở về"},
    {"english": "be in the mood for doing something", "cefr": "B2", "phonetics": "/bi ɪn ðə mud fɔr ˈduɪŋ ˈsʌmθɪŋ/", "vietnamese": "Có hứng thú làm gì"},
    {"english": "all walks of life", "cefr": "C1", "phonetics": "/ɔl wɔks ʌv laɪf/", "vietnamese": "Mọi tầng lớp xã hội"},
]

# ─── LESSON 5 ───────────────────────────────────────────────────────────────
L5_VOCAB = [
    {"english": "genre (n)", "cefr": "B2", "phonetics": "/ˈʒɑːnrə/", "vietnamese": "Thể loại"},
    {"english": "tension (n)", "cefr": "B2", "phonetics": "/ˈtenʃn/", "vietnamese": "Sự căng thẳng"},
    {"english": "blockbuster (n)", "cefr": "C1", "phonetics": "/ˈblɑːkbʌstər/", "vietnamese": "Bom tấn (phim, sách,…)"},
    {"english": "addictive (adj)", "cefr": "C1", "phonetics": "/əˈdɪktɪv/", "vietnamese": "Gây nghiện"},
    {"english": "plot (n)", "cefr": "B1", "phonetics": "/plɑːt/", "vietnamese": "Tình tiết, cốt truyện"},
    {"english": "bookworm (n)", "cefr": "NA", "phonetics": "/ˈbʊkwɜːrm/", "vietnamese": "Mọt sách"},
    {"english": "protagonist (n)", "cefr": "C2", "phonetics": "/prəˈtæɡənɪst/", "vietnamese": "Nhân vật chính"},
    {"english": "portable (adj)", "cefr": "C1", "phonetics": "/ˈpɔːrtəbl/", "vietnamese": "Có thể cầm tay"},
    {"english": "antique (adj)", "cefr": "B1", "phonetics": "/ænˈtiːk/", "vietnamese": "Cổ"},
    {"english": "eye-catching (adj)", "cefr": "NA", "phonetics": "/ˈaɪkætʃɪŋ/", "vietnamese": "Bắt mắt"},
    {"english": "high-quality (adj)", "cefr": "B1", "phonetics": "/ˌhaɪˈkwɑːləti/", "vietnamese": "Chất lượng cao"},
    {"english": "state-of-the-art (adj)", "cefr": "C1", "phonetics": "/ˌsteɪt əv ði ˈɑːrt/", "vietnamese": "Tiên tiến nhất hiện có"},
    {"english": "innovative (adj)", "cefr": "B2", "phonetics": "/ˈɪnəveɪtɪv/", "vietnamese": "Cách tân, có tính đổi mới"},
    {"english": "practical (adj)", "cefr": "B1", "phonetics": "/ˈpræktɪkl/", "vietnamese": "Thực tế"},
    {"english": "informative (adj)", "cefr": "C1", "phonetics": "/ɪnˈfɔːrmətɪv/", "vietnamese": "Cung cấp nhiều tin tức"},
    {"english": "beneficial (adj)", "cefr": "B2", "phonetics": "/ˌbenɪˈfɪʃl/", "vietnamese": "Có ích"},
    {"english": "perspective (n)", "cefr": "B2", "phonetics": "/pərˈspektɪv/", "vietnamese": "Góc nhìn"},
]
L5_COLL = [
    {"english": "skim through something", "cefr": "B2", "phonetics": "/skɪm θru ˈsʌmθɪŋ/", "vietnamese": "Đọc lướt qua cái gì"},
    {"english": "adapted from something", "cefr": "B2", "phonetics": "/əˈdæptɪd frʌm ˈsʌmθɪŋ/", "vietnamese": "Được chuyển thể từ cái gì"},
    {"english": "catch the latest movie", "cefr": "B1", "phonetics": "/kæʧ ðə ˈleɪtəst ˈmuvi/", "vietnamese": "Xem bộ phim mới ra mắt"},
    {"english": "catch one's attention", "cefr": "B2", "phonetics": "/kæʧ wʌnz əˈtɛnʃən/", "vietnamese": "Khiến ai đó chú ý"},
    {"english": "from cover to cover", "cefr": "B2", "phonetics": "/frʌm ˈkʌvər tu ˈkʌvər/", "vietnamese": "Từ đầu đến cuối"},
    {"english": "catch one's eye", "cefr": "B2", "phonetics": "/kæʧ wʌnz aɪ/", "vietnamese": "Bắt mắt ai đó"},
    {"english": "a waste of money", "cefr": "B1", "phonetics": "/ə weɪst ʌv ˈmʌni/", "vietnamese": "Không đáng tiền, phí tiền"},
    {"english": "hand something down", "cefr": "B2", "phonetics": "/hænd ˈsʌmθɪŋ daʊn/", "vietnamese": "Truyền lại cái gì cho thành viên nhỏ"},
    {"english": "pick something up", "cefr": "B2", "phonetics": "/pɪk ˈsʌmθɪŋ ʌp/", "vietnamese": "Mua cái gì đó, thường với giá rẻ"},
    {"english": "come across something", "cefr": "B2", "phonetics": "/kʌm əˈkrɔs ˈsʌmθɪŋ/", "vietnamese": "Tình cờ nhìn thấy, tìm thấy gì đó"},
]
L5_PHRASES = [
    "I'm going to describe my all-time favorite… which was …",
    "When it comes to…, I'd like to bring up/mention…",
    "… comes/springs to my mind when asked about …",
    "It brings me a sense of joy and gratitude every time I see it.",
    "To me, … has great emotional/sentimental values…",
    "This movie/book holds a special place in my heart.",
    "The movie's/book's captivating storytelling kept me engaged from beginning to end.",
]

# ─── LESSON 6 ───────────────────────────────────────────────────────────────
L6_COLL = [
    {"english": "fact checking", "cefr": "B2", "phonetics": "/ˈfækt ʧekɪŋ/", "vietnamese": "Kiểm tra sự thật"},
    {"english": "resemblance (n)", "cefr": "B2", "phonetics": "/rɪˈzembləns/", "vietnamese": "Sự giống nhau"},
    {"english": "compensate for", "cefr": "B2", "phonetics": "/ˈkɑmpənˌseɪt fɔr/", "vietnamese": "Đền bù cho"},
    {"english": "queue up for something", "cefr": "B1", "phonetics": "/kju ʌp fɔr ˈsʌmθɪŋ/", "vietnamese": "Xếp hàng chờ cái gì"},
    {"english": "get carried away", "cefr": "B2", "phonetics": "/ɡɛt tu ˈkærid əˈweɪ/", "vietnamese": "Hào hứng quá mức"},
    {"english": "get rid of bad luck", "cefr": "B2", "phonetics": "/ɡɛt rɪd ʌv bæd lʌk/", "vietnamese": "Trừ xui"},
    {"english": "foster growth", "cefr": "B2", "phonetics": "/ˈfɑstər ɡroʊθ/", "vietnamese": "Thúc đẩy sự phát triển"},
    {"english": "voice one's displeasure", "cefr": "C1", "phonetics": "/vɔɪs wʌnz dɪˈsplɛʒər/", "vietnamese": "Bày tỏ sự không hài lòng"},
    {"english": "grab the chance", "cefr": "B2", "phonetics": "/ɡræb ðə ʧæns/", "vietnamese": "Nắm bắt cơ hội"},
    {"english": "have a blast", "cefr": "B2", "phonetics": "/hæv ə blæst/", "vietnamese": "Vui cực kỳ"},
    {"english": "dispel ghosts and evils", "cefr": "C1", "phonetics": "/dɪˈspɛl ɡoʊsts ænd ˈivəlz/", "vietnamese": "Xua đuổi ma quỷ"},
    {"english": "a sense of camaraderie", "cefr": "C1", "phonetics": "/ə sɛns ʌv ˌkɑməˈrɑdəri/", "vietnamese": "Tình bạn bè, đồng đội"},
    {"english": "potentially fatal allergy", "cefr": "B2", "phonetics": "/pəˈtɛnʃəli ˈfeɪtl ˈælərʤi/", "vietnamese": "Dị ứng có thể gây chết người"},
    {"english": "a case of mistaken identity", "cefr": "B2", "phonetics": "/ə keɪs ʌv mɪsˈteɪkən aɪˈdɛntəti/", "vietnamese": "Nhầm lẫn danh tính"},
    {"english": "superstitious belief", "cefr": "B2", "phonetics": "/ˌsupərˈstɪʃəs bɪˈlif/", "vietnamese": "Tín ngưỡng mê tín"},
    {"english": "bask in warmth from friends and families' company", "cefr": "C1", "phonetics": "/bæsk ɪn wɔrmθ frʌm frɛndz ænd ˈfæməliz ˈkʌmpəni/", "vietnamese": "Tận hưởng sự ấm áp từ bạn bè và gia đình"},
    {"english": "hit the ceiling", "cefr": "B2", "phonetics": "/hɪt ðə ˈsilɪŋ/", "vietnamese": "Tức giận cực độ"},
    {"english": "go through the roof", "cefr": "B2", "phonetics": "/ɡoʊ θru ðə ruf/", "vietnamese": "Tăng vọt / tức giận"},
]

# ─── LESSON 7 ───────────────────────────────────────────────────────────────
L7_VOCAB = [
    {"english": "budget (n)", "cefr": "B1", "phonetics": "/ˈbʌdʒɪt/", "vietnamese": "Kinh phí"},
    {"english": "recreational (adj)", "cefr": "C2", "phonetics": "/ˌrekriˈeɪʃənl/", "vietnamese": "Thuộc về giải trí"},
    {"english": "stamina (n)", "cefr": "C1", "phonetics": "/ˈstæmɪnə/", "vietnamese": "Sức bền"},
    {"english": "stretch (v)", "cefr": "B2", "phonetics": "/stretʃ/", "vietnamese": "Giãn cơ"},
    {"english": "motivation (n)", "cefr": "B2", "phonetics": "/ˌmoʊtɪˈveɪʃn/", "vietnamese": "Động lực"},
    {"english": "cardiovascular (adj)", "cefr": "NA", "phonetics": "/ˌkɑːrdioʊˈvæskjələr/", "vietnamese": "Thuộc về tim mạch"},
    {"english": "light-hearted (adj)", "cefr": "B2", "phonetics": "/ˌlaɪtˈhɑːrtɪd/", "vietnamese": "Nhẹ nhàng"},
    {"english": "road trip (n)", "cefr": "B1", "phonetics": "/ˈroʊd ˌtrɪp/", "vietnamese": "Chuyến đi bằng đường bộ"},
    {"english": "intrepid (adj)", "cefr": "C1", "phonetics": "/ɪnˈtrepɪd/", "vietnamese": "Quả cảm"},
    {"english": "burn calories (v)", "cefr": "NA", "phonetics": "/bɜrn ˈkæləriz/", "vietnamese": "Đốt cháy calo"},
    {"english": "core muscles (n)", "cefr": "B2", "phonetics": "/kɔr ˈmʌsəlz/", "vietnamese": "Các cơ cốt lõi"},
    {"english": "lush forest (n)", "cefr": "C1", "phonetics": "/lʌʃ ˈfɔːrɪst/", "vietnamese": "Khu rừng xanh tươi"},
    {"english": "get lean (v)", "cefr": "B2", "phonetics": "/ɡet lin/", "vietnamese": "Có ít hoặc không có mỡ thừa"},
]
L7_COLL = [
    {"english": "hustle and bustle", "cefr": "B2", "phonetics": "/ˈhʌsəl ænd ˈbʌsəl/", "vietnamese": "Hối hả và nhộn nhịp"},
    {"english": "break the journey", "cefr": "B2", "phonetics": "/breɪk ðə ˈʤɜrni/", "vietnamese": "Dừng nghỉ chân"},
    {"english": "do the sights", "cefr": "B2", "phonetics": "/du ðə saɪts/", "vietnamese": "Đi ngắm danh lam thắng cảnh"},
    {"english": "a low-cost airline", "cefr": "B2", "phonetics": "/ə ˌloʊˈkɑːst ˈerlaɪn/", "vietnamese": "Hãng hàng không giá rẻ"},
    {"english": "get itchy feet", "cefr": "NA", "phonetics": "/ɡet ˈɪʧi fit/", "vietnamese": "Luôn muốn đi đây đó"},
    {"english": "boost someone's spirit", "cefr": "B2", "phonetics": "/bust ˈsʌmˌwʌn ˈspɪrɪt/", "vietnamese": "Khiến ai phấn chấn"},
]
L7_PHRASES = [
    "I'd like to talk about an activity that I'm into doing in my leisure time.",
    "The best thing about … is …",
    "… allows us to express ourselves creatively and emotionally.",
    "After burying myself in work, I decided to … to let off steam.",
    "I find that this activity does wonders for …",
    "It has been a lifelong dream for me to …",
    "I'd like to talk about a trip which I'm really looking forward to.",
    "This trip would be a transformative/precious/valuable experience.",
    "I can hardly contain my excitement.",
]

# ─── LESSON 8 ───────────────────────────────────────────────────────────────
L8_VOCAB = [
    {"english": "mapping (n)", "cefr": "NA", "phonetics": "/ˈmæpɪŋ/", "vietnamese": "Khả năng định hướng"},
    {"english": "instinct (n)", "cefr": "C1", "phonetics": "/ˈɪnstɪŋkt/", "vietnamese": "Bản năng"},
    {"english": "variation (n)", "cefr": "B2", "phonetics": "/ˌveriˈeɪʃn/", "vietnamese": "Sự biến đổi, biến thể"},
    {"english": "well-being (n)", "cefr": "C1", "phonetics": "/ˈwel biːɪŋ/", "vietnamese": "Sức khỏe"},
    {"english": "disorder (n)", "cefr": "B2", "phonetics": "/dɪsˈɔːrdər/", "vietnamese": "Sự rối loạn"},
    {"english": "stimulation (n)", "cefr": "NA", "phonetics": "/ˌstɪmjuˈleɪʃn/", "vietnamese": "Sự kích thích, khuyến khích"},
    {"english": "stamina (n)", "cefr": "C1", "phonetics": "/ˈstæmɪnə/", "vietnamese": "Sức bền"},
    {"english": "resilience (n)", "cefr": "C2", "phonetics": "/rɪˈzɪliəns/", "vietnamese": "Sự kiên nhẫn, kiên cường"},
    {"english": "simulation (n)", "cefr": "C1", "phonetics": "/ˌsɪmjuˈleɪʃn/", "vietnamese": "Sự mô phỏng"},
    {"english": "collaboration (n)", "cefr": "C1", "phonetics": "/kəˌlæbəˈreɪʃn/", "vietnamese": "Sự cộng tác"},
    {"english": "genetic (adj)", "cefr": "B2", "phonetics": "/dʒəˈnetɪk/", "vietnamese": "Thuộc gien, thuộc di truyền"},
    {"english": "innate (adj)", "cefr": "C2", "phonetics": "/ɪˈneɪt/", "vietnamese": "Bẩm sinh"},
    {"english": "spatial (adj)", "cefr": "NA", "phonetics": "/ˈspeɪʃl/", "vietnamese": "Thuộc về không gian"},
    {"english": "timid (adj)", "cefr": "C1", "phonetics": "/ˈtɪmɪd/", "vietnamese": "Rụt rè, nhút nhát"},
    {"english": "cognitive (adj)", "cefr": "C1", "phonetics": "/ˈkɑːɡnətɪv/", "vietnamese": "Liên quan đến nhận thức"},
    {"english": "applicable (adj)", "cefr": "C1", "phonetics": "/əˈplɪkəbl/", "vietnamese": "Có thể áp dụng được"},
    {"english": "superior (adj)", "cefr": "C1", "phonetics": "/suːˈpɪriər/", "vietnamese": "Vượt trội"},
    {"english": "mundane (adj)", "cefr": "C1", "phonetics": "/mʌnˈdeɪn/", "vietnamese": "Nhỏ nhặt, tầm thường"},
    {"english": "absent-minded (adj)", "cefr": "NA", "phonetics": "/ˌæbsənt ˈmaɪndɪd/", "vietnamese": "Đãng trí"},
    {"english": "retentive (adj)", "cefr": "NA", "phonetics": "/rɪˈtentɪv/", "vietnamese": "Có khả năng nhớ các sự kiện lâu"},
    {"english": "immersive (adj)", "cefr": "NA", "phonetics": "/ɪˈmɜːrsɪv/", "vietnamese": "Nhập vai"},
    {"english": "impair (v)", "cefr": "NA", "phonetics": "/ɪmˈper/", "vietnamese": "Làm suy yếu, suy giảm"},
    {"english": "derive (v)", "cefr": "B2", "phonetics": "/dɪˈraɪv/", "vietnamese": "Nhận được từ, lấy được từ"},
    {"english": "strive (v)", "cefr": "C1", "phonetics": "/straɪv/", "vietnamese": "Cố gắng, phấn đấu"},
    {"english": "instil (v)", "cefr": "NA", "phonetics": "/ɪnˈstɪl/", "vietnamese": "Làm thấm nhuần"},
    {"english": "cater (v)", "cefr": "C1", "phonetics": "/ˈkeɪtər/", "vietnamese": "Phục vụ cho"},
    {"english": "inherit (v)", "cefr": "B2", "phonetics": "/ɪnˈherɪt/", "vietnamese": "Kế thừa, thừa hưởng"},
]
L8_COLL = [
    {"english": "innate sense of direction", "cefr": "C2", "phonetics": "/ɪˈneɪt sɛns ʌv dəˈrɛkʃən/", "vietnamese": "Khả năng định hướng bẩm sinh"},
    {"english": "spatial memory", "cefr": "NA", "phonetics": "/ˈspeɪʃəl ˈmɛməri/", "vietnamese": "Trí nhớ không gian"},
    {"english": "cognitive mapping", "cefr": "C1", "phonetics": "/ˈkɑɡnɪtɪv ˈmæpɪŋ/", "vietnamese": "Khả năng định hướng trong tiềm thức"},
    {"english": "memory-impairing illness", "cefr": "NA", "phonetics": "/ˈmɛməri ɪmˈpɛrɪŋ ˈɪlnəs/", "vietnamese": "Bệnh suy giảm trí nhớ"},
    {"english": "brain-boosting diet", "cefr": "NA", "phonetics": "/breɪn ˈbustɪŋ ˈdaɪət/", "vietnamese": "Chế độ ăn tăng cường trí não"},
    {"english": "emotional disorder", "cefr": "B2", "phonetics": "/ɪˈmoʊʃənəl dɪˈsɔrdər/", "vietnamese": "Rối loạn cảm xúc"},
    {"english": "retentive memory", "cefr": "NA", "phonetics": "/rɪˈtentɪv ˈmeməri/", "vietnamese": "Trí nhớ dai"},
    {"english": "immersive experiences", "cefr": "NA", "phonetics": "/ɪˈmɜːrsɪv ɪkˈspɪriənsɪz/", "vietnamese": "Trải nghiệm sâu sắc"},
    {"english": "realistic simulation", "cefr": "C1", "phonetics": "/ˌriəˈlɪstɪk ˌsɪmjəˈleɪʃən/", "vietnamese": "Mô phỏng hiện thực"},
    {"english": "keep a cool head", "cefr": "NA", "phonetics": "/kip ə kul hɛd/", "vietnamese": "Bình tĩnh"},
    {"english": "lose one's sense of direction", "cefr": "B2", "phonetics": "/luz wʌnz sɛns ʌv dəˈrɛkʃən/", "vietnamese": "Mất phương hướng"},
    {"english": "trust one's instinct", "cefr": "C1", "phonetics": "/trʌst wʌnz ˈɪnstɪŋkt/", "vietnamese": "Tin vào bản năng của ai"},
    {"english": "inherit genetic variations", "cefr": "B2", "phonetics": "/ɪnˈhɛrət ʤəˈnɛtɪk ˌvɛriˈeɪʃənz/", "vietnamese": "Kế thừa các biến thể di truyền"},
    {"english": "derive satisfaction from the journey", "cefr": "B2", "phonetics": "/dɪˈraɪv ˌsætɪsˈfækʃən frʌm ðə ˈʤɜrni/", "vietnamese": "Nhận được sự hài lòng từ quá trình"},
    {"english": "increase physical stamina", "cefr": "C1", "phonetics": "/ˈɪnˌkris ˈfɪzɪkəl ˈstæmənə/", "vietnamese": "Gia tăng sức bền thể chất"},
    {"english": "strive for victory", "cefr": "C2", "phonetics": "/straɪv fɔr ˈvɪktəri/", "vietnamese": "Phấn đấu giành chiến thắng"},
    {"english": "instil values", "cefr": "NA", "phonetics": "/ɪnˈstɪl ˈvæljuz/", "vietnamese": "Làm thấm nhuần các giá trị"},
    {"english": "work towards a common objective", "cefr": "NA", "phonetics": "/wɜrk təˈwɔrdz ə ˈkɑmən əbˈʤɛktɪv/", "vietnamese": "Làm việc hướng tới mục tiêu chung"},
    {"english": "push one's boundaries", "cefr": "C1", "phonetics": "/pʊʃ wʌnz ˈbaʊndəriz/", "vietnamese": "Vượt qua giới hạn của bản thân"},
    {"english": "step out of one's comfort zone", "cefr": "B2", "phonetics": "/stɛp aʊt ʌv wʌnz ˈkʌmfərt zoʊn/", "vietnamese": "Bước ra khỏi vùng an toàn"},
    {"english": "you name it", "cefr": "NA", "phonetics": "/ju neɪm ɪt/", "vietnamese": "Vân vân"},
    {"english": "on end", "cefr": "NA", "phonetics": "/ɑn ɛnd/", "vietnamese": "Liên tục"},
    {"english": "the in thing", "cefr": "NA", "phonetics": "/ði ɪn θɪŋ/", "vietnamese": "Trào lưu, phổ biến"},
]
L8_PHRASES = [
    "**ARERC technique:** Answer → Reason → Example(s) → Consequence",
    "**7 Part 3 question types:** Opinion, Evaluation, Future, Cause & effect, Hypothetical, Compare & contrast, Talking about other people",
    "That's a very interesting/tough question.",
    "I've never thought about this before.",
    "To be honest, it's not an area of my interest.",
    "I have to admit that I don't know much about this topic, but I think …",
    "As far as I'm concerned, ….",
    "There are a myriad of reasons why…, chief among these is …",
    "The reasons vary, but I guess the most … one is that ….",
    "Definitely yes / Absolutely yes / Of course.",
    "I couldn't agree more. / I totally agree.",
    "Many people think that…, but I don't buy it.",
    "I'm afraid I disagree. / I totally disagree with this viewpoint.",
    "To be honest, I would have to say it really depends …",
    "There are tons/loads of …, chief among these is …",
    "It varies from individual to individual.",
]

# ─── LESSON 10 ──────────────────────────────────────────────────────────────
L10_VOCAB = [
    {"english": "diligence (n)", "cefr": "C1", "phonetics": "/ˈdɪlɪdʒəns/", "vietnamese": "Sự siêng năng, cần cù"},
    {"english": "get in touch with", "cefr": "B1", "phonetics": "/ɡɛt ɪn tʌʧ wɪð/", "vietnamese": "Liên lạc với"},
    {"english": "catch up with", "cefr": "B1", "phonetics": "/kæʧ ʌp wɪð/", "vietnamese": "Gặp gỡ, cập nhật tin tức"},
    {"english": "worth every penny", "cefr": "B2", "phonetics": "/wɜrθ ˈɛvri ˈpɛni/", "vietnamese": "Đáng từng đồng tiền"},
    {"english": "let off steam", "cefr": "B2", "phonetics": "/lɛt ɔf stim/", "vietnamese": "Xả hơi, giải tỏa căng thẳng"},
    {"english": "do wonders for", "cefr": "B2", "phonetics": "/du ˈwʌndərz fɔr/", "vietnamese": "Có tác dụng tốt cho"},
]
L10_PHRASES = [
    "Review: Part 2 structure → Introduction → Story → Opinion",
    "Review: Part 3 structure → ARERC (Answer, Reason, Example, Consequence)",
    "Combine vocabulary from Lessons 3–9 when answering cue cards.",
    "Use buying-time phrases before answering difficult Part 3 questions.",
]

# Lesson 3 & 9 - image PDFs, structure phrases only
L3_PHRASES = [
    "**Part 2 — Describe a person structure:** Introduction → Story (who/when/where) → Description (appearance, personality) → Opinion",
    "I'm going to talk about a person who has had a significant impact on my life.",
    "What strikes me most about him/her is …",
    "He/She has always been someone I look up to because …",
    "In terms of appearance, he/she is …",
    "Personality-wise, I would describe him/her as …",
]
L9_PHRASES = [
    "**Part 3 continued** — pair with Lesson 8 frameworks.",
    "On the one hand … On the other hand …",
    "While some people believe …, others argue that …",
    "It is often said that …, however, I think …",
    "From my perspective, the key issue is …",
]


def parse_simon_phrases(text: str) -> list[dict]:
    topics = []
    # Body sections start after "Positives of Advertising"
    body = text.split("Positives of Advertising")[0]
    body = text[text.find("Positives of Advertising"):] if "Positives of Advertising" in text else text

    # Find topic blocks in content pages
    pattern = re.compile(
        r"(Positives of [A-Za-z][^\n]+|Negatives of [A-Za-z][^\n]+|Opinions about [A-Za-z][^\n]+|"
        r"Genetically-Modified \(GM\) Foods: [A-Za-z]+|The Future of [A-Za-z][^\n]+|"
        r"Against [A-Za-z][^\n]+|Unemployment Benefits: [A-Za-z]+|Self-employment|Unemployment)\n",
        re.M,
    )
    current_topic = "General"
    topic_phrases: dict[str, list[str]] = defaultdict(list)

    for line in text.split("\n"):
        line = line.strip()
        m = re.match(r"^(\d+)\. ([A-Za-z].+)$", line)
        if m and len(m.group(2)) < 60 and "Page" not in m.group(2):
            current_topic = m.group(2).strip()
            continue
        if len(line) > 25 and line[0].isupper() and not line.startswith("Page") and "ielts" not in line.lower():
            if not re.match(r"^(Positives|Negatives|Opinions|Contents|Against|The Future)", line):
                topic_phrases[current_topic].append(line)

    for topic, phrases in topic_phrases.items():
        if phrases and topic not in ("Contents", "es"):
            topics.append({"topic": topic, "phrases": dedupe_phrases(phrases)[:25]})
    return topics


def dedupe_phrases(phrases: list[str]) -> list[str]:
    seen = set()
    out = []
    for p in phrases:
        k = p.lower().strip()
        if k and k not in seen and len(k) > 20:
            seen.add(k)
            out.append(p)
    return out


def main():
    os.makedirs(VOCAB_DIR, exist_ok=True)
    stats = []

    lessons = [
        ("fighter-lesson-01-wh-questions", "Lesson 1 — Review Technique: Wh-questions (Part 1)",
         "[Fighter 5] LS_Speaking - Lesson 1. Review technique Wh-questions.pdf", L1_VOCAB, L1_COLL, None, "**Focus:** Part 1 Wh-questions — describing people & daily life"),
        ("fighter-lesson-02-review-techniques", "Lesson 2 — Review Techniques (Part 1)",
         "[Fighter 5] LS- Speaking - Lesson 2. Review techniques.pdf", L2_VOCAB, L2_COLL, L2_PHRASES, "**Focus:** Technology, Entertainment & Transport"),
        ("fighter-lesson-03-part2-people", "Lesson 3 — Part 2: Review People (Monologue)",
         "[Fighter 5] LS - Speaking - Lesson 3. Part 2 - Review people monologue.pdf", None, None, L3_PHRASES,
         "_Note: PDF is image-based; vocabulary in original file. Below are structure phrases._"),
        ("fighter-lesson-04-places", "Lesson 4 — Part 2: Review Places",
         "[Fighter 5] LS- Speaking - Lesson 4. Review places.pdf", None, L4_COLL, None, "**Focus:** Describing places"),
        ("fighter-lesson-05-part2-things", "Lesson 5 — Part 2: Review Things",
         "[Fighter 5] LS - Speaking - Lesson 5. Part 2 - Review things.pdf", L5_VOCAB, L5_COLL, L5_PHRASES, "**Focus:** Physical & concept objects (books, films)"),
        ("fighter-lesson-06-past-events", "Lesson 6 — Part 2: Review Past Events & Activities",
         "[Fighter 5] LS- Speaking - Lesson 6. Review past events and activities.pdf", None, L6_COLL, None, "**Focus:** Past events & memorable experiences"),
        ("fighter-lesson-07-events-activities", "Lesson 7 — Part 2: Review Events & Activities",
         "[Fighter 5] LS - Speaking - Lesson 7. Part 2 - Review events and activities (2).pdf", L7_VOCAB, L7_COLL, L7_PHRASES, "**Focus:** Present hobbies & future plans"),
        ("fighter-lesson-08-part3-1", "Lesson 8 — Speaking Part 3 (1)",
         "[Fighter 5] LS- Speaking - Lesson 8. Speaking part 3 (1).pdf", L8_VOCAB, L8_COLL, L8_PHRASES, "**Focus:** Part 3 discussion — ARERC technique"),
        ("fighter-lesson-09-part3-2", "Lesson 9 — Speaking Part 3 (2)",
         "[Fighter 5] LS - Speaking - Lesson 9. Speaking Part 3 (2).pdf", None, None, L9_PHRASES,
         "_Note: PDF is image-based. Pair with Lesson 8._"),
        ("fighter-lesson-10-review-part2-3", "Lesson 10 — Review Speaking Part 2 + 3",
         "[Fighter 5] LS- Speaking - Lesson 10. Review speaking part 2 + 3.pdf", L10_VOCAB, None, L10_PHRASES, "**Focus:** Combined Part 2 + 3 review"),
    ]

    for slug, title, source, vocab, coll, phrases, extra in lessons:
        v, c, p = write_lesson(slug, title, source, vocab, coll, phrases, extra)
        stats.append((slug, v, c, p))
        print(f"{slug}: {v} vocab, {c} coll, {p} phrases")

    # Simon source
    simon_topics = parse_simon_phrases(text_from_simon())
    lines = [
        "# IELTS Simon — Ideas for IELTS Topics",
        "",
        "> Source: `BAND 6.5 TO 9.0 IDEAS FOR IELTS TOPIC - IELTS SIMON (1).pdf`",
        "> File: `simon-ideas-for-ielts-topics.md`",
        "",
        "Key phrases and ideas by topic — useful for Part 3 discussion.",
        "",
    ]
    total_phrases = 0
    for t in simon_topics:
        lines.append(f"## {t['topic']}")
        lines.append("")
        for p in t["phrases"]:
            lines.append(f"- {p}")
        lines.append("")
        total_phrases += len(t["phrases"])

    with open(os.path.join(VOCAB_DIR, "simon-ideas-for-ielts-topics.md"), "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    print(f"simon-ideas-for-ielts-topics: {len(simon_topics)} topics, {total_phrases} phrases")

    # README index
    readme = [
        "# IELTS Speaking — Vocabulary",
        "",
        "Vocabulary, collocations, and key phrases from **IELTS Fighter lessons** and **IELTS Simon**.",
        "",
        "## Lesson Files (IELTS Fighter)",
        "",
        "| File | Focus | Vocab | Collocations | Phrases |",
        "|------|-------|-------|--------------|---------|",
    ]
    focus_map = {
        "fighter-lesson-01-wh-questions": "Part 1 — Wh-questions",
        "fighter-lesson-02-review-techniques": "Part 1 — Tech & Transport",
        "fighter-lesson-03-part2-people": "Part 2 — People",
        "fighter-lesson-04-places": "Part 2 — Places",
        "fighter-lesson-05-part2-things": "Part 2 — Things",
        "fighter-lesson-06-past-events": "Part 2 — Past events",
        "fighter-lesson-07-events-activities": "Part 2 — Activities",
        "fighter-lesson-08-part3-1": "Part 3 — Discussion",
        "fighter-lesson-09-part3-2": "Part 3 — More practice",
        "fighter-lesson-10-review-part2-3": "Part 2 + 3 Review",
    }
    for slug, v, c, p in stats:
        readme.append(f"| [{slug}.md]({slug}.md) | {focus_map.get(slug,'')} | {v} | {c} | {p} |")
    readme += [
        "",
        "## Source Files",
        "",
        f"- [simon-ideas-for-ielts-topics.md](simon-ideas-for-ielts-topics.md) — {len(simon_topics)} topics, {total_phrases} key phrases",
        f"- [all-vocabulary.md](all-vocabulary.md) — combined quick reference",
        "",
    ]
    with open(os.path.join(VOCAB_DIR, "README.md"), "w") as f:
        f.write("\n".join(readme))

    # Combined all-vocabulary
    combined = ["# All Vocabulary — Combined Quick Reference", "", "> Merged from all IELTS Fighter lessons.", ""]
    all_vocab = L1_VOCAB + L2_VOCAB + L5_VOCAB + L7_VOCAB + L8_VOCAB + L10_VOCAB
    all_coll = L1_COLL + L2_COLL + L4_COLL + L5_COLL + L6_COLL + L7_COLL + L8_COLL
    combined.append("## All Vocabulary")
    combined.append("")
    for e in all_vocab:
        combined.append(f"- **{e['english']}** `{e['phonetics']}` — {e['vietnamese']}")
    combined.append("")
    combined.append("## All Collocations")
    combined.append("")
    for e in all_coll:
        combined.append(f"- *{e['english']}* `{e['phonetics']}` — {e['vietnamese']}")
    with open(os.path.join(VOCAB_DIR, "all-vocabulary.md"), "w") as f:
        f.write("\n".join(combined) + "\n")

    print(f"\nDone — files in {VOCAB_DIR}")


def text_from_simon() -> str:
    path = os.path.join(BASE, "extra material /BAND 6.5 TO 9.0 IDEAS FOR IELTS TOPIC - IELTS SIMON (1).pdf")
    return "\n".join(p.get_text() for p in fitz.open(path))


if __name__ == "__main__":
    main()
