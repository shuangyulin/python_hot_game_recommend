export default {
	baseUrl: 'http://localhost:8080/django0gx5n277/',
	name: '/django0gx5n277',
	indexNav: [
		{
			name: '游戏信息',
			url: '/index/gameinfo',
		},
		{
			name: '社区互动',
			url: '/index/forum'
		}, 
		{
			name: '游戏资讯',
			url: '/index/news'
		},
		{
			name: '意见反馈',
			url: '/index/messages'
		},
	],
	cateList: [
		{
			name: '社区互动',
			refTable: 'forumtype',
			refColumn: 'typename',
		},
		{
			name: '游戏资讯',
			refTable: 'newstype',
			refColumn: 'typename',
		},
	]
}
