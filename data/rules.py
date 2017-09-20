# -*- coding: utf-8 -*-
################################### Notice ####################################
# `en2zh` is a function which changes the English url into Chinese one.
# `screenshot_js` steps:
# 1) Let the screen focus on the item.
# 2) Set the price back to origin if it is on sale.
# 3) Delete the elements about discount.
#
# TODO: net-a-porter.com, if only change /en/ to /zh/, the spider will be baned.
# But I don't know why yet.
###############################################################################
import re


website_rules = {
    'www.lanecrawford.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'.com', '.com.cn', x),
        'type': 'Retailer',
        'brand': '.lc-product-brand-refresh',
        'text_css': {
            'title': '.lc-product-short-description-refresh',
            'desc': '.text-paragraph',
            'details': '.sizeAndFit li',
        },
        'photo_urls_css': '.hero-carousel__img::attr(data-xl)',
        'screenshot_js': '''window.scrollBy(0, 174);
if ($(".discounted-price").text().replace(/(^\s*)|(\s*$)/g, '').length != 0){
    $(".sale-price").text($(".discounted-price").text());
    $(".discounted-price").remove();
    $(".save-percentage").remove();
};''',
    },

    'www.net-a-porter.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'/us/en/', '/cn/zh/', x),
        'type': 'Retailer',
        'brand': '.designer-name span',
        'text_css': {
            'title': '.product-name',
            'desc': '.show-hide-content .wrapper p',
            'details': '.show-hide-content .wrapper ul li',
        },
        'photo_urls_css': '.thumbnail-image::attr(src)',
        'handle_photo_urls': lambda x: [re.sub(r'_\w\w.jpg', '_xl.jpg', url) for url in x],
        'screenshot_js': '''window.scrollBy(0, 174);
if ($(".container-title .sale") != 0){
    $(".container-title .sale-price").text($(".container-title .full-price").text());
    $(".container-title .sale").removeClass("sale");
    $(".container-title s").remove();
    $(".container-title .discount").remove();
}''',
    },

    'www.farfetch.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'.com', '.com/cn', x),
        'type': 'Retailer',
        'brand': '.detail-brand a',
        'text_css': {
            'title': '.detail-brand span',
            'desc': '.product-detail p[itemprop*=description]',
            'details': '.product-detail-dl dd',
        },
        'photo_urls_css': '.sliderProduct-link img::attr(data-fullsrc)',
        'screenshot_js': '''window.scrollBy(0, 50);
if ($(".js-discount-label").html().replace(/(^\W\s*)|(\W\s*$)/g, '').length != 0){
    $(".js-discount-label").html($(".js-price-without-promotion").html());
    $(".js-price-without-promotion").remove();
    $(".js-price").remove();
}''',
    },

    'www.shopbop.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'www.', 'cn.', x),
        'type': 'Retailer',
        'brand': '.brand-heading a',
        'text_css': {
            'title': '.product-title',
            'desc': '.content[itemprop*=description]',
            'details': 'div[id*=modelSize]',
        },
        'photo_urls_css': 'script[type*=text\/javascript]',
        'photo_urls_re': 'zoom": "(\S+)"',
        'screenshot_js': '''window.scrollBy(0, 150);
if ($(".originalRetailPrice").length != 0){
    $(".originalRetailPrice").removeClass("originalRetailPrice")
    $(".priceBlock:eq(1)").remove();
}''',
    },

    'www.mytheresa.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'/en-us/', '/zh-cn/', x),
        'type': 'Retailer',
        'brand': '.product-shop .product-designer a',
        'text_css': {
            'title': '.product-shop .product-name span',
            'desc': '.product-description',
            'details': '.featurepoints li',
        },
        'photo_urls_css': '.gallery-image::attr(src)',
        'handle_photo_urls': lambda x: [re.sub(r'/1088/1088/66/', u'/2176/2176/90/', url) for url in x],
        'screenshot_js': '''window.scrollBy(0, 240);''',
    },

    'us.burberry.com': {
        'has_zh_maybe': False,
        'en2zh': lambda x: re.sub(r'us.', 'cn.', x) + '?locale=zh-CN',
        'type': 'Official',
        'brand': u'BURBERRY',
        'text_css': {
            'title': 'h1',
            'desc': '.cell-paragraph_description li',
            'details': '.cell-paragraph_details li',
        },
        'text_css_zh': {
            'title': 'h1',
            'desc': '.accordion-tab_content p',
            'details': '.accordion-tab_sub-item li',
        },
        'photo_urls_css': 'div::attr(data-zoom-src)',
        'screenshot_js': ''';''',
    },

    'www.luisaviaroma.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'/lang_EN/', '/lang_ZH/', x),
        'type': 'Retailer',
        'brand': '#sp_a_designer',
        'text_css': {
            'title': '#sp_a_category',
            'desc': None,
            'details': '#sp_details li',
        },
        'photo_urls_css': 'script',
        'photo_urls_re': '"PhotosAll":\[(\S+)\],"PhotosByColor"',
        # 'handle_photo_urls': lambda x: ['https://images.luisaviaroma.com/Zoom' + url for url in re.split('[",]+', x[0]) if url],
        'screenshot_js': '''window.scrollBy(0, 50);
$('#footer_tc_privacy_button').click();
$('table').remove();
var span_price = $('#sp_span_price');
var price_text = span_price.text();
var minus_index = price_text.indexOf('-')
if (minus_index != -1){
    price_text.replace(price_text.slice(minus_index), '');
    $('#sp_span_discountedprice').remove();
}''',
    },

    'www.matchesfashion.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 a',
        'text_css': {
            'title': 'h1 span',
            'desc': '.scroller-content p',
            'details': None,
        },
        'photo_urls_css': '.gallery-panel__main-image-carousel img::attr(src)',
        'screenshot_js': '''$('.mfp-wrap').remove();
$('.mfp-bg').remove();
window.scrollBy(0, 174);
if ($('.pdp-price__hilite').length != 0){
    var price_text = $('strike:eq(0)').text();
    $('.pdp-price').text(price_text);
}''',
    },

    'www.ssense.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 a',
        'text_css': {
            'title': 'h2',
            'desc': '.product-description-text',
            'details': None,
        },
        'photo_urls_css': '.image-wrapper img::attr(data-src)',
        'screenshot_js': ''';''',
    },

    'www.lyst.com': {
        'has_zh_maybe': False,
        'type': 'Pool',
        'brand': 'h1 div[itemprop=brand] a, h3 span[itemprop=brand] a',
        'text_css': {
            'title': 'h1 div[itemprop=name], h1 span[itemprop=name]',
            'desc': 'div[itemprop=description] p',
            'details': None,
        },
        'photo_urls_css': '.image-gallery-thumbnail::attr(data-full-image-url), .image-gallery__carousel__scroll-wrapper__image a::attr(href)',
        'screenshot_js': ''';''',
    },

    'www.lyst.ca': {
        'has_zh_maybe': False,
        'type': 'Pool',
        'brand': 'h1 div[itemprop=brand] a, h3 span[itemprop=brand] a',
        'text_css': {
            'title': 'h1 div[itemprop=name], h1 span[itemprop=name]',
            'desc': 'div[itemprop=description] p',
            'details': None,
        },
        'photo_urls_css': '.image-gallery-thumbnail::attr(data-full-image-url), .image-gallery__carousel__scroll-wrapper__image a::attr(href)',
        'screenshot_js': ''';''',
    },

    'www.shopsplash.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'Alexis',
        'text_css': {
            'title': 'h1[itemprop=name]',
            'desc': 'div.into',
            'details': None,
        },
        'photo_urls_css': 'a.cloud-zoom-gallery::attr(href)',
        'screenshot_js': ''';''',
    },

    'www.stellamccartney.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'Stella Mccartney',
        'text_css': {
            'title': 'h1.title span',
            'desc': '.contentDesc .editorialdescription .value',
            'details': '.contentDesc .details .value',
        },
        'photo_urls_css': 'img::attr(srcset)',
        'photo_urls_re': r',(\S+) 1920w',
        'screenshot_js': ''';''',
    },

    'www.neimanmarcus.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'span[itemprop=brand], span[itemprop=brand] a',
        'text_css': {
            'title': 'span[itemprop=name]',
            'desc': None,
            'details': 'div[itemprop=description] li',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(data-zoom-url)',
        'screenshot_js': '''window.scrollBy(0, 150);''',
    },

    'www.fwrd.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.designer_brand',
        'text_css': {
            'title': '.product_name',
            'desc': None,
            'details': '.product_detail li',
        },
        'photo_urls_css': '.product_z img::attr(src)',
        'screenshot_js': '''window.scrollBy(0, 50);''',
    },

    'www.madstyle.com.au': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MAD STYLE',
        'text_css': {
            'title': 'h1',
            'desc': None,
            'details': '.std',
        },
        'photo_urls_css': '.gallery-image::attr(data-zoom-image)',
        'screenshot_js': '''window.scrollBy(0, 50);''',
    },

    'www.theoutnet.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 a',
        'text_css': {
            'title': 'h1 span',
            'desc': None,
            'details': '.accordion-content li',
        },
        'photo_urls_css': '#large-image img::attr(data-src)',
        'screenshot_js': ''';''',
    },

    'www.armani.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ARMANI',
        'text_css': {
            'title': 'h1',
            'desc': '.descriptionContent',
            'details': '.descriptionList li',
        },
        'photo_urls_css': 'img.thumb::attr(src)',
        'handle_photo_urls': lambda x: [re.sub(r'_13_', '_16_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'us.zimmermannwear.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ZIMMERMANN',
        'text_css': {
            'title': 'h1',
            'desc': 'p.itemDesc',
            'details': '.small p',
        },
        'photo_urls_css': '.showmainImg::attr(data-fullimg)',
        'screenshot_js': '''window.scrollBy(0, 100);''',
    },

    'www.stylebop.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.h1 a',
        'text_css': {
            'title': 'h1.h2',
            'desc': '.desc-content li',
            'details': None,
        },
        'photo_urls_css': 'img::attr(data-zoom-image)',
        'screenshot_js': '''window.scrollBy(0, 300);''',
    },

    'www.tedbaker.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'TED BAKER',
        'text_css': {
            'title': 'h2.summary',
            'desc': '.description',
            'details': '#product_details li',
        },
        'photo_urls_css': '.pdp_main_slider img::attr(ng-src)',
        'screenshot_js': ''';''',
    },

    'www.kenzo.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'KENZO',
        'text_css': {
            'title': 'h1',
            'desc': '.kz-pp-fiche-desc div',
            'details': '.kz-pp-fiche-compo p',
        },
        'photo_urls_css': '.kz-pp-image img::attr(src)',
        'screenshot_js': ''';''',
    },

    'cn.sportmax.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'SPORTMAX',
        'text_css': {
            'title': '.c-product-data .h3-like',
            'desc': '.description',
            'details': 'li',
        },
        'photo_urls_css': 'a::attr(data-zoom)',
        'screenshot_js': '''window.scrollBy(0, 220);''',
    },

    'www.melijoe.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'a[itemprop=brand]',
        'text_css': {
            'title': 'h1',
            'desc': None,
            'details': '.detail-bloc-item .value',
        },
        'photo_urls_css': '.swiper-slide::attr(data-zoom)',
        'screenshot_js': '''window.scrollBy(0, 100);''',
    },

    'www.modaoperandi.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.designer_title',
        'text_css': {
            'title': '.product_title',
            'desc': '.description_text p',
            'details': None,
        },
        'photo_urls_css': 'img.primary_image_display::attr(src)',
        'screenshot_js': '''window.scrollBy(0, 50);''',
    },

    'www.fashionbarnshop.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1',
        'text_css': {
            'title': 'h1',
            'desc': None,
            'details': '#tabs-1 li',
        },
        'photo_urls_css': '.slide a::attr(data-zoom-image)',
        'screenshot_js': '''window.scrollBy(0, 150);''',
    },

    'www.amazon.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '#productTitle',
        'text_css': {
            'title': '#productTitle',
            'desc': None,
            'details': '#feature-bullets .a-list-item',
        },
        'photo_urls_css': 'script',
        'photo_urls_re': 'hiRes":"(\S+)","thumb',
        'screenshot_js': '''window.scrollBy(0, 200);''',
    },

    'www.aliceandolivia.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ALICE AND OLIVIA',
        'text_css': {
            'title': 'h1',
            'desc': '.box font span',
            'details': '.detail-box li',
        },
        'photo_urls_css': '.slide img::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.gucci.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'GUCCI',
        'text_css': {
            'title': 'h1',
            'desc': '.product-detail p',
            'details': '.product-detail li',
        },
        'photo_urls_css': 'img.item-content::attr(data-src_standard_retina)',
        'screenshot_js': ''';''',
    },

    'www.selfridges.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 .brand a',
        'text_css': {
            'title': 'h1 .description',
            'desc': 'p[itemprop=description]',
            'details': '.productDetails script',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'screenshot_js': '''window.scrollBy(0, 200);''',
    },

    'us.sandro-paris.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'SANDRO',
        'text_css': {
            'title': 'h1',
            'desc': None,
            'details': 'h2.detaildesc',
        },
        'photo_urls_css': '.productlargeimgdata::attr(data-lgimg)',
        'handle_photo_urls': lambda x: x[0].split('|'),
        'screenshot_js': ''';''',
    },

    'uk.sandro-paris.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'SANDRO',
        'text_css': {
            'title': 'h1',
            'desc': None,
            'details': 'h2.detaildesc',
        },
        'photo_urls_css': '.productlargeimgdata::attr(data-lgimg)',
        'handle_photo_urls': lambda x: x[0].split('|'),
        'screenshot_js': ''';''',
    },

    'www.dereklam.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'DEREK LAM',
        'text_css': {
            'title': 'h1',
            'desc': None,
            'details': '.os-product-description li',
        },
        'photo_urls_css': 'script',
        'photo_urls_re': '''"ImageUrl":"(\S+)","ImageThumbUrl"''',
        'screenshot_js': ''';''',
    },

    'www.tibi.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'TIBI',
        'text_css': {
            'title': 'h1',
            'desc': '.std p',
            'details': '.std li',
        },
        'photo_urls_css': 'img.gallery-image::attr(data-zoom-image)',
        'screenshot_js': ''';''',
    },

    'www.flannels.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '#ProductName',
        'text_css': {
            'title': '#ProductName',
            'desc': 'span[itemprop=description] p',
            'details': 'span[itemprop=description] li',
        },
        'photo_urls_css': '#piThumbList a::attr(href)',
        'handler_photo_urls': lambda x: [re.sub(r'_l_', '_xxl_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.bluefly.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'p[itemprop=brand] a',
        'text_css': {
            'title': 'title',
            'desc': 'div[itemprop=description]',
            'details': 'ul[data-ui=accordion-content] li',
        },
        'photo_urls_css': 'a::attr(data-zoom-image)',
        'screenshot_js': ''';''',
    },

    'www.tadashishoji.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'TADASHI SHOJI',
        'text_css': {
            'title': 'h1',
            'desc': '.inner',
            'details': '.inner li',
        },
        'photo_urls_css': 'a::attr(data-zoom-image)',
        'screenshot_js': ''';''',
    },

    'www.montaignemarket.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'small.pr_brand a[itemprop=brand]',
        'text_css': {
            'title': 'h1',
            'desc': 'span[itemprop=description] p',
            'details': None,
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.vincecamuto.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'VINCE CAMUTO',
        'text_css': {
            'title': 'h1',
            'desc': '.product-tabs',
            'details': '.product-tabs li',
        },
        'photo_urls_css': 'li img::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.bottegaveneta.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'BOTTEGA VENETA',
        'text_css': {
            'title': '.inner.modelName',
            'desc': None,
            'details': '.tab-body .value',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'photo_urls_re': '\S+.jpg$',
        'handle_photo_urls': lambda x: [re.sub(r'_7_', '_15_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.johnlewis.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.mod a img::attr(title)',
        'text_css': {
            'title': 'h1 span',
            'desc': 'span[itemprop=description] p',
            'details': 'dd',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+_main\$$',
        'handle_photo_urls': lambda x: [re.sub(r'_main', '_lrg', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.harrods.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 .brand',
        'text_css': {
            'title': '.productname',
            'desc': '.description',
            'details': '#details li',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+\$thumbnail\$$',
        'handle_photo_urls': lambda x: [re.sub(r'thumbnail', 'fullScreen', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.zadig-et-voltaire.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ZADIG ET VOLTAIRE',
        'text_css': {
            'title': 'h1',
            'desc': '.short-description p',
            'details': None,
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+530x795\S+',
        'handle_photo_urls': lambda x: [re.sub(r'\/530x795', '', url) for url in x],
        'screenshot_js': ''';''',
    },

    'intl.aritzia.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ARITZIA',
        'text_css': {
            'title': 'h1',
            'desc': '.pdp-tab-content p',
            'details': '.pdp-tab-content li',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+thumbnail\S+',
        'handle_photo_urls': lambda x: [re.sub(r'thumbnail', 'large', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.mcq.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MCQ',
        'text_css': {
            'title': 'h1 span',
            'desc': '.descriptions .value',
            'details': '.compositionInfo .text',
        },
        'photo_urls_css': 'img::attr(srcset)',
        'photo_urls_re': ',(\S+) 2x$',
        'screenshot_js': ''';''',
    },

    'shop.nordstrom.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h2 span',
        'text_css': {
            'title': 'h1',
            'desc': 'div[itemprop=description] p',
            'details': 'li',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '(\S+Zoom\S+.jpg)\?\S+',
        'screenshot_js': ''';''',
    },

    'us.maje.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MAJE',
        'text_css': {
            'title': 'h1 span',
            'desc': '.tabs-content p',
            'details': '.tabs-content span',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '(\S+.jpg)\?\S+',
        'screenshot_js': ''';''',
    },

    'www.ministryofstyle.com.au': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MINISTRY OF STYLE',
        'text_css': {
            'title': '.styledetails h2',
            'desc': '.description',
            'details': None,
        },
        'photo_urls_css': 'a::attr(zoom)',
        'screenshot_js': ''';''',
    },

    'www.bally.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'BALLY',
        'text_css': {
            'title': 'h1',
            'desc': '#tab1 p',
            'details': '#tab2 p',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'photo_urls_re': '(\S+.jpg)\?',
        'screenshot_js': ''';''',
    },

    'www.katespade.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'KATE SPADE',
        'text_css': {
            'title': 'h1',
            'desc': '#small-details',
            'details': '#small-description li',
        },
        'photo_urls_css': 'img::attr(data-cloudzoom)',
        'photo_urls_re': "image: '(\S+)'",
        'screenshot_js': ''';''',
    },

    'www.bcbg.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'BCBG',
        'text_css': {
            'title': 'h1',
            'desc': '#tab2 p',
            'details': '#tab2 li',
        },
        'photo_urls_css': 'img[itemprop]::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.miumiu.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MIU MIU',
        'text_css': {
            'title': 'h2',
            'desc': 'p.desc',
            'details': None,
        },
        'photo_urls_css': 'a::attr(data-zoom)',
        'screenshot_js': ''';''',
    },

    'www.equipmentfr.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'EQUIPMENT',
        'text_css': {
            'title': 'span[itemprop=name]',
            'desc': 'span.desc',
            'details': '.product-description li',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+633x\S+.jpg$',
        'screenshot_js': ''';''',
    },

    'www.moschino.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MOSCHINO',
        'text_css': {
            'title': 'h1 span',
            'desc': '#tab-body p',
            'details': '#tab-body span',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+_13_\w\.jpg',
        'handle_photo_urls': lambda x: [re.sub(r'_13_', '_14_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.revolve.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'span[property=brand]',
        'text_css': {
            'title': 'h1',
            'desc': None,
            'details': '.product-details__list li',
        },
        'photo_urls_css': 'a::attr(data-zoom-image)',
        'screenshot_js': ''';''',
    },

    'marimekkovancouver.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MARIMEKKO',
        'text_css': {
            'title': 'h1',
            'desc': 'div[itemprop=description] span',
            'details': None,
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+_small.jpg',
        'handle_photo_urls': lambda x: [re.sub(r'_small', '_1024x1024', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.31philliplim.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'3.1 PHILLIP LIM',
        'text_css': {
            'title': 'h2',
            'desc': '.accordion-body p',
            'details': '.accordion-body li',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+.jpg$',
        'screenshot_js': ''';''',
    },
}

###############################################################################
############################ Rules with problems ##############################
#
# neimanmarcus.com will banned your IP and redirect to a url that let you to
# input CAPCHA. We can change IP by middlewares, but there is still something
# wrong with `photo_urls_css`, `brand` and get a screenshot by selenium.
#    'www.neimanmarcus.com': {
#        'has_zh_maybe': False,
#        'type': 'Retailer',
#        'brand': 'span[itemprop=brand], span[itemprop=brand] a',
#        'text_css': {
#            'title': 'span[itemprop=name]',
#            'desc': None,
#            'details': 'div[itemprop=description] li',
#        },
#        'photo_urls_css': 'img[itemprop=image]::attr(data-zoom-url)',
#        'screenshot_js': '''window.scrollBy(0, 150);
#$('.item-label').remove();
#$('ins.sale-text').remove();
#$('.tooltipHolder').remove();
#''',
#    },
