var rule={
    title:'1985',
    host:'https://www.1985.one/',
    url:'/vodtype/fyclass-fypage.html',
    searchUrl:'/vodsearch/page/fypage/wd/**.html',
    class_name:'电影&电视剧&动漫&综艺',
    class_url:'1&2&4&3',
    searchable: 2,//是否启用全局搜索,
    quickSearch: 0,//是否启用快速搜索,
    filterable: 0,//是否启用分类筛选,
    lazy:'js:var html=JSON.parse(request(input).match(/r player_.*?=(.*?)</)[1]);var url=html.url;if(html.encrypt=="1"){url=unescape(url)}else if(html.encrypt=="2"){url=unescape(base64Decode(url))}if(/m3u8|mp4/.test(url)){input=url}else{input}',
    play_parse: true,
    lazy: '',
    limit: 6,
    推荐: '.module-list;.module-items&&.module-item;a&&title;img&&data-src;.module-item-text&&Text;a&&href',
    double: true, // 推荐内容是否双层定位
    一级: '.module-items .module-item;a&&title;img&&data-src;.module-item-text&&Text;a&&href',
    二级: {
        "title": "h1&&Text;.tag-link&&Text",
        "img": ".module-item-pic&&img&&data-src",
        "desc": ".video-info-items:eq(3)&&Text;;;.video-info-actor:eq(1)&&Text;.video-info-actor:eq(0)&&Text",
        "content": ".vod_content&&Text",
        "tabs": ".module-tab-item",
        "lists": ".module-player-list:eq(#id)&&.scroll-content&&a"
    },
    搜索: '.module-items&&.module-search-item;h3&&Text;img&&data-src;.video-serial&&Text;h3&&a&&href',
}
