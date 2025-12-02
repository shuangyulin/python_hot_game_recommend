<template>
	<div>
		<div id="particles"></div>
		<div class="login-container">
			<el-form class="login_form animate__animated animate__backInDown">
				<div class="login_form2">
					<div class="title-container">基于Python的热门游戏推荐系统的设计与实现登录</div>
					<div v-if="loginType==1" class="list-item">
						<div class="lable">
							<span class="icon iconfont icon-touxiang09"></span>
						</div>
						<input placeholder="请输入账号：" name="username" type="text" v-model="rulesForm.username">
					</div>
					<div v-if="loginType==1" class="list-item">
						<div class="lable">
							<span class="icon iconfont icon-chakan13"></span>
						</div>
						<div class="password-box">
							<input placeholder="请输入密码：" name="password" :type="showPassword?'text':'password'" v-model="rulesForm.password">
							<span class="icon iconfont" :class="showPassword?'icon-liulan13':'icon-liulan17'" @click="showPassword=!showPassword"></span>
						</div>
					</div>

					<div class="list-item " v-if="roles.length>1">
						<div class="lable">
							<span class="icon iconfont icon-touxiang15"></span>
						</div>
						<div prop="loginInRole" class="list-type">
							<el-radio v-if="loginType==1||(loginType==2&&item.roleName!='管理员')" v-for="item in roles" v-bind:key="item.roleName" v-model="rulesForm.role" :label="item.roleName">{{item.roleName}}</el-radio>
						</div>
					</div>

		
					<div class="login-btn">
						<div class="login-btn1">
							<el-button v-if="loginType==1" type="primary" @click="login()" class="loginInBt">登录</el-button>
						</div>
						<div class="login-btn2">
						</div>
						<div class="login-btn3">
						</div>
					</div>
				</div>
			</el-form>
		</div>
	</div>
</template>
<script>
	import 'animate.css'
	import menu from "@/utils/menu";
	require('@/utils/particles.js')
	export default {
		data() {
			return {
				verifyCheck2: false,
				flag: false,
				baseUrl:this.$base.url,
				loginType: 1,
				rulesForm: {
					username: "",
					password: "",
					role: "",
				},
				menus: [],
				roles: [],
				tableName: "",
				showPassword: false,
				particlesJson: {"retina_detect":true,"particles":{"number":{"density":{"value_area":800,"enable":true},"value":120},"move":{"straight":false,"random":false,"bounce":false,"enable":true,"attract":{"rotateX":3000,"enable":false,"rotateY":3000},"speed":2,"direction":"none","out_mode":"out"},"color":{"value":"#000"},"shape":{"image":{"width":100,"src":"img/github.svg","height":100},"polygon":{"nb_sides":5},"type":"circle","stroke":{"color":"#000000","width":0}},"size":{"anim":{"size_min":0,"sync":false,"enable":false,"speed":20},"random":false,"value":2},"line_linked":{"width":1,"distance":100,"color":"#000","opacity":1,"enable":true},"opacity":{"anim":{"opacity_min":0,"sync":false,"enable":false,"speed":1},"random":false,"value":0.5}},"interactivity":{"detect_on":"canvas","events":{"resize":true,"onclick":{"mode":"push","enable":true},"onhover":{"mode":"grab","enable":true}},"modes":{"grab":{"distance":100,"line_linked":{"opacity":1}},"bubble":{"duration":0.7,"distance":200,"size":80,"opacity":0,"speed":3},"repulse":{"duration":0.4,"distance":200},"push":{"particles_nb":4},"remove":{"particles_nb":2}}}}
			};
		},
		mounted() {
			let menus = menu.list();
			this.menus = menus;

			for (let i = 0; i < this.menus.length; i++) {
				if (this.menus[i].hasBackLogin=='是') {
					this.roles.push(this.menus[i])
				}
			}

			particlesJS('particles',this.particlesJson);
		},
		created() {

		},
		destroyed() {
		},
		components: {
		},
		methods: {

			//注册
			register(tableName){
				this.$storage.set("loginTable", tableName);
				this.$router.push({path:'/register',query:{pageFlag:'register'}})
			},
			// 登陆
			login() {

				if (!this.rulesForm.username) {
					this.$message.error("请输入用户名");
					return;
				}
				if (!this.rulesForm.password) {
					this.$message.error("请输入密码");
					return;
				}
				if(this.roles.length>1) {
					if (!this.rulesForm.role) {
						this.$message.error("请选择角色");
						return;
					}

					let menus = this.menus;
					for (let i = 0; i < menus.length; i++) {
						if (menus[i].roleName == this.rulesForm.role) {
							this.tableName = menus[i].tableName;
						}
					}
				} else {
					this.tableName = this.roles[0].tableName;
					this.rulesForm.role = this.roles[0].roleName;
				}
		
				this.loginPost()
			},
			loginPost() {
				this.$http({
					url: `${this.tableName}/login?username=${this.rulesForm.username}&password=${this.rulesForm.password}`,
					method: "post"
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.$storage.set("Token", data.token);
						this.$storage.set("role", this.rulesForm.role);
						this.$storage.set("sessionTable", this.tableName);
						this.$storage.set("adminName", this.rulesForm.username);
						this.$nextTick(()=>{
							this.$http({
								url: this.tableName + '/session',
								method: "get"
							}).then(({
								data
							}) => {
								if (data && data.code === 0) {
									if(this.tableName == 'yonghu') {
										this.$storage.set('headportrait',data.data.touxiang)
									}
									if(this.tableName == 'users') {
										this.$storage.set('headportrait',data.data.image)
									}
									this.$storage.set('userForm',JSON.stringify(data.data))
									this.$storage.set('userid',data.data.id);
								} else {
									let message = this.$message
									message.error(data.msg);
								}
								if(this.boardAuth('hasBoard','查看',this.rulesForm.role)) {
									this.$router.replace({ path: "/board" });
								}else {
									this.$router.replace({ path: "/" });
								}
							});
						})
					} else {
						this.$message.error(data.msg);
					}
				});
			},
		}
	}
</script>

<style lang="scss" scoped>
.login-container {
	min-height: 100vh;
	position: relative;
	background-repeat: no-repeat;
	background-position: center center;
	background-size: cover;
	background: #fff;
	background-repeat: no-repeat;
	background-size: cover;
	background: #fff;
	display: flex;
	width: 100%;
	min-height: 100vh;
	align-items: center;
	background-position: center center;

	.login_form {
		padding: 120px 40px 40px 40px;
		margin: auto;
		z-index: 1000;
		display: flex;
		flex-wrap: wrap;
		border-radius: 0;
		box-shadow: inset 0px 0px 0px 0px #000;
		flex-direction: column;
		background: #F2F8FF;
		width: 680px;
		align-items: center;
		position: relative;
		height: auto;
		.login_form2 {
			background: none;
			width: 500px;
		}
		.title-container {
			padding: 0 40px;
			margin: 0 0 20px 0;
			color: #000;
			top: 60px;
			left: 0;
			background: none;
			font-weight: 500;
			width: 100%;
			font-size: 28px;
			line-height: 40px;
			position: absolute;
			text-align: center;
		}
		.list-item {
			padding: 0;
			margin: 15px 0 ;
			background: none;
			display: flex;
			width: 100%;
			align-items: center;
			position: relative;
			height: 60px;
			.lable {
				border: 0 ;
				margin: 10px;
				z-index: 2;
				color: #333333;
				letter-spacing: 1px;
				font-size: 16px;
				border-radius: 20px;
				left: 10px;
				background: #DCEEFF;
				width: auto;
				position: absolute;
				text-align: center;
				min-width: 60px;
				.icon {
					color: #364E64;
					width: 64px;
					font-size: 14px;
					line-height: 44px;
				}
			}
			input {
				border: 1px solid #0000FF;
				border-radius: 60px;
				padding: 0 100px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 16px;
				height: 60px;
			}
			input:focus {
				border: 1px solid #0000FF;
				border-radius: 60px;
				padding: 0 100px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 16px;
				height: 60px;
			}
			.password-box {
				display: flex;
				width: 100%;
				align-items: center;
				input {
					border: 1px solid #0000FF;
					border-radius: 60px;
					padding: 0 100px;
					outline: none;
					color: #666;
					flex: 1;
					background: none;
					width: 100%;
					font-size: 14px;
					line-height: 60px;
					height: 60px;
				}
				input:focus {
					border: 1px solid #0000FF;
					border-radius: 60px;
					padding: 0 100px;
					outline: none;
					color: #666;
					flex: 1;
					background: none;
					width: 100%;
					font-size: 14px;
					line-height: 60px;
					height: 60px;
				}
				.iconfont {
					cursor: pointer;
					z-index: 1;
					color: #000;
					top: 0;
					font-size: 16px;
					line-height: 60px;
					position: absolute;
					right: 10px;
				}
			}
			input::placeholder {
				color: #999;
				font-size: 14px;
			}
		}
		.list-type {
			border: 1px solid #0000FF;
			padding: 0 100px;
			margin: 15px 0;
			color: #666;
			display: flex;
			font-size: 16px;
			min-height: 60px;
			flex-wrap: wrap;
			border-radius: 60px;
			outline: none;
			flex: 1;
			width: 100%;
			align-items: center;
			height: auto;
			/deep/ .el-radio__input .el-radio__inner {
				background: #A4A4A4;
				border-color: #666;
			}
			/deep/ .el-radio__input.is-checked .el-radio__inner {
				background: #0000FF;
				border-color: #0d6efd;
			}
			/deep/ .el-radio__label {
				color: #A4A4A4;
				font-size: 16px;
			}
			/deep/ .el-radio__input.is-checked+.el-radio__label {
				color: #0000FF;
				font-size: 16px;
			}
		}
		.login-btn {
			margin: 20px auto;
			display: flex;
			width: 100%;
			justify-content: center;
			align-items: center;
			flex-wrap: wrap;
			.login-btn1 {
				margin: 15px 0;
				width: 100%;
				order: 1;
			}
			.login-btn2 {
				display: flex;
				width: 100%;
				justify-content: space-between;
				align-items: center;
				flex-wrap: wrap;
				order: 3;
			}
			.login-btn3 {
				width: 100%;
				order: 2;
			}
			.loginInBt {
				border: 0px solid rgba(0, 0, 0, 1);
				cursor: pointer;
				border-radius: 60px;
				padding: 0 10px;
				margin: 0;
				color: #FFFFFF;
				background: #0000FF;
				font-weight: 500;
				width: 100%;
				font-size: 28px;
				height: 60px;
			}
			.loginInBt:hover {
				opacity: 0.8;
			}
			.register {
				border: 2px solid #B8B8B8;
				cursor: pointer;
				border-radius: 4px;
				padding: 10px;
				margin: 0 10px;
				color: #B8B8B8;
				background: none;
				width: auto;
				font-size: 16px;
				height: 34px;
			}
			.register:hover {
				opacity: 0.8;
			}
			.forget {
				border: 0;
				cursor: pointer;
				border-radius: 0;
				padding: 0;
				margin: 15px 0;
				color: #000000;
				background: none;
				font-weight: 400;
				width: 100%;
				font-size: 16px;
				text-align: center;
				height: 34px;
			}
			.forget:hover {
				color: #0d6efd;
				opacity: 1;
			}
		}
	}
}

	#particles{
		background-repeat: no-repeat;
		z-index: 1;
		background-size: cover;
		width: 100%;
		position: absolute;
		background-position: 50% 50%;
		height: 100%;
	}
</style>
