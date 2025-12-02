<template>
	<div>
		<div id="particles"></div>
		<div class="register-container">
			<el-form v-if="pageFlag=='register'" ref="ruleForm" class="rgs-form animate__animated animate__backInDown" :model="ruleForm" :rules="rules">
				<div class="rgs-form2">
					<div class="title">基于Python的热门游戏推荐系统的设计与实现注册</div>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('yonghuming')?'required':''">用户名：</div>
						<el-input  v-model="ruleForm.yonghuming"  autocomplete="off" placeholder="用户名"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('mima')?'required':''">密码：</div>
						<el-input  v-model="ruleForm.mima"  autocomplete="off" placeholder="密码"  type="password"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('mima')?'required':''">确认密码：</div>
						<el-input  v-model="ruleForm.mima2" autocomplete="off" placeholder="确认密码" type="password" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('xingming')?'required':''">姓名：</div>
						<el-input  v-model="ruleForm.xingming"  autocomplete="off" placeholder="姓名"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('touxiang')?'required':''">头像：</div>
						<file-upload
							tip="点击上传头像"
							action="file/upload"
							:limit="3"
							:multiple="true"
							:fileUrls="ruleForm.touxiang?ruleForm.touxiang:''"
							@change="yonghutouxiangUploadChange"
						></file-upload>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('xingbie')?'required':''">性别：</div>
						<el-select v-model="ruleForm.xingbie" placeholder="请选择性别" >
							<el-option
								v-for="(item,index) in yonghuxingbieOptions"
								v-bind:key="index"
								:label="item"
								:value="item">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('nianling')?'required':''">年龄：</div>
						<el-input  v-model.number="ruleForm.nianling"  autocomplete="off" placeholder="年龄"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('youxiang')?'required':''">邮箱：</div>
						<el-input  v-model="ruleForm.youxiang"  autocomplete="off" placeholder="邮箱"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('shouji')?'required':''">手机：</div>
						<el-input  v-model="ruleForm.shouji"  autocomplete="off" placeholder="手机"  type="text"  />
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<button type="button" class="r-btn" @click="login()">注册</button>
						</div>
						<div class="register-btn2">
							<div class="r-login" @click="close()">已有账号，点击登录</div>
						</div>
					</div>
				</div>
			</el-form>
		</div>
	</div>
</template>

<script>
	import 'animate.css'
	require('@/utils/particles.js');
export default {
	data() {
		return {
			ruleForm: {
			},
			forgetForm: {},
            pageFlag : '',
			tableName:"",
			rules: {},
            yonghuxingbieOptions: [],
			particlesJson: {"retina_detect":true,"particles":{"number":{"density":{"value_area":800,"enable":true},"value":120},"move":{"straight":false,"random":false,"bounce":false,"enable":true,"attract":{"rotateX":3000,"enable":false,"rotateY":3000},"speed":2,"direction":"none","out_mode":"out"},"color":{"value":"#000"},"shape":{"image":{"width":100,"src":"img/github.svg","height":100},"polygon":{"nb_sides":5},"type":"circle","stroke":{"color":"#000000","width":0}},"size":{"anim":{"size_min":0,"sync":false,"enable":false,"speed":20},"random":false,"value":2},"line_linked":{"width":1,"distance":100,"color":"#000","opacity":1,"enable":true},"opacity":{"anim":{"opacity_min":0,"sync":false,"enable":false,"speed":1},"random":false,"value":0.5}},"interactivity":{"detect_on":"canvas","events":{"resize":true,"onclick":{"mode":"push","enable":true},"onhover":{"mode":"grab","enable":true}},"modes":{"grab":{"distance":100,"line_linked":{"opacity":1}},"bubble":{"duration":0.7,"distance":200,"size":80,"opacity":0,"speed":3},"repulse":{"duration":0.4,"distance":200},"push":{"particles_nb":4},"remove":{"particles_nb":2}}}}
		};
	},
	mounted(){
		particlesJS('particles',this.particlesJson);
		this.pageFlag = this.$route.query.pageFlag
		if(this.$route.query.pageFlag=='register'){
			
			let table = this.$storage.get("loginTable");
			this.tableName = table;
			if(this.tableName=='yonghu'){
				this.ruleForm = {
					yonghuming: '',
					mima: '',
					xingming: '',
					touxiang: '',
					xingbie: '',
					nianling: '',
					youxiang: '',
					shouji: '',
				}
			}
			if ('yonghu' == this.tableName) {
				this.rules.yonghuming = [{ required: true, message: '请输入用户名', trigger: 'blur' }]
			}
			if ('yonghu' == this.tableName) {
				this.rules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }]
			}
			if ('yonghu' == this.tableName) {
				this.rules.xingming = [{ required: true, message: '请输入姓名', trigger: 'blur' }]
			}
			this.yonghuxingbieOptions = "男,女".split(',')
		}
	},
	created() {
	},
	destroyed() {
		  	},
	methods: {
		changeRules(name){
			if(this.rules[name]){
				return true
			}
			return false
		},
		// 获取uuid
		getUUID () {
			return new Date().getTime();
		},
		close(){
			this.$router.push({ path: "/login" });
		},
        yonghutouxiangUploadChange(fileUrls) {
            this.ruleForm.touxiang = fileUrls;
        },

        // 多级联动参数


		// 注册
		login() {
			var url=this.tableName+"/register";
			if((!this.ruleForm.yonghuming) && `yonghu` == this.tableName){
				this.$message.error(`用户名不能为空`);
				return
			}
			if((!this.ruleForm.mima) && `yonghu` == this.tableName){
				this.$message.error(`密码不能为空`);
				return
			}
			if((this.ruleForm.mima!=this.ruleForm.mima2) && `yonghu` == this.tableName){
				this.$message.error(`两次密码输入不一致`);
				return
			}
			if((!this.ruleForm.xingming) && `yonghu` == this.tableName){
				this.$message.error(`姓名不能为空`);
				return
			}
            if(this.ruleForm.touxiang!=null) {
                this.ruleForm.touxiang = this.ruleForm.touxiang.replace(new RegExp(this.$base.url,"g"),"");
            }
			if(`yonghu` == this.tableName && this.ruleForm.nianling &&(!this.$validate.isIntNumer(this.ruleForm.nianling))){
				this.$message.error(`年龄应输入整数`);
				return
			}
			if(`yonghu` == this.tableName && this.ruleForm.youxiang &&(!this.$validate.isEmail(this.ruleForm.youxiang))){
				this.$message.error(`邮箱应输入邮件格式`);
				return
			}
			if(`yonghu` == this.tableName && this.ruleForm.shouji &&(!this.$validate.isMobile(this.ruleForm.shouji))){
				this.$message.error(`手机应输入手机格式`);
				return
			}
			this.$http({
				url: url,
				method: "post",
				data:this.ruleForm
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.$message({
						message: "注册成功",
						type: "success",
						duration: 1500,
						onClose: () => {
							this.$router.replace({ path: "/login" });
						}
					});
				} else {
					this.$message.error(data.msg);
				}
			});
		}
	}
};
</script>

<style lang="scss" scoped>
.register-container {
	position: relative;
	background: #fff;
	background-repeat: no-repeat;
	background-size: cover;
	background: #fff;
	display: flex;
	width: 100%;
	min-height: 100vh;
	align-items: center;
	background-position: center center;
	.rgs-form {
		.rgs-form2 {
		background: none;
		width: 500px;
		}
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
		.title {
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
			border-radius: 8px;
			padding: 0;
			margin: 15px 0;
			background: none;
			display: flex;
			width: calc(100% - 0px);
			align-items: center;
			position: relative;
			flex-wrap: wrap;
			/deep/ .el-form-item__content {
				display: block;
				width: 100%;
			}
			.lable {
				padding: 0 5px 0 0;
				color: #364E64;
				left: 10px;
				width: 130px;
				font-size: 14px;
				line-height:  60px;
				position: absolute !important;
				text-align: left;
			}
			.el-input {
				width: 100%;
			}
			.el-input /deep/ .el-input__inner {
				border: 1px solid #0000FF;
				border-radius: 60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-input /deep/ .el-input__inner:focus {
				border: 1px solid #0000FF;
				border-radius: 60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-input-number {
				width: 100%;
			}
			.el-input-number /deep/ .el-input__inner {
				text-align: center;
				border: 1px solid #0000FF;
				border-radius: 60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-input-number /deep/ .el-input__inner:focus {
				border: 1px solid #0000FF;
				border-radius: 60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-input-number /deep/ .el-input-number__decrease {
				display: none;
			}
			.el-input-number /deep/ .el-input-number__increase {
				display: none;
			}
			.el-select {
				width: 100%;
			}
			.el-select /deep/ .el-input__inner {
				border: 1px solid #0000FF;
				border-radius:  60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-select /deep/ .el-input__inner:focus {
				border: 1px solid #0000FF;
				border-radius:  60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-date-editor {
				width: 100%;
			}
			.el-date-editor /deep/ .el-input__inner {
				border: 1px solid #0000FF;
				border-radius:  60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-date-editor /deep/ .el-input__inner:focus {
				border: 1px solid #0000FF;
				border-radius:  60px;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height:  60px;
			}
			.el-date-editor.el-input {
				width: 100%;
			}
			/deep/ .el-upload--picture-card {
				background: transparent;
				border: 0;
				border-radius: 0;
				width: auto;
				height: auto;
				line-height: initial;
				vertical-align: middle;
			}
			/deep/ .upload .upload-img {
				border: 1px solid #0000FF;
				padding: 0 72px;
				margin: 0 0 0 80px;
				color: 60px;
				flex: 1;
				background: none;
				font-size: 16px;
				line-height: 60px;
				height: 60px;
			}
			/deep/ .el-upload-list .el-upload-list__item {
				border: 1px solid #0000FF;
				padding: 0 72px;
				margin: 0 0 0 80px;
				color: 60px;
				flex: 1;
				background: none;
				font-size: 16px;
				line-height: 60px;
				height: 60px;
			}
			/deep/ .el-upload .el-icon-plus {
				border: 1px solid #0000FF;
				padding: 0 72px;
				margin: 0 0 0 80px;
				color: 60px;
				flex: 1;
				background: none;
				font-size: 16px;
				line-height: 60px;
				height: 60px;
			}
			/deep/ .el-upload__tip {
				color: #666;
				display: none;
				font-size: 15px;
			}
			/deep/ .el-input__inner::placeholder {
				color: #999;
				font-size: 14px;
			}
			.required {
				position: relative;
			}
			.required::after{
				color: red;
				left: -10px;
				line-height: 60px ;
				position: inherit;
				content: "*";
				order: -1;
			}
			.editor {
				border: 1px solid #0000FF;
				border-radius: 60px;
				background: none;
				width: 500px;
				height: auto;
			}
			.editor>.avatar-uploader {
				line-height: 0;
				height: 0;
			}
		}
		.list-item.email {
			input {
				border: 1px solid #0000FF;
				border-radius: 60px ;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height: 60px ;
			}
			input:focus {
				border: 1px solid #0000FF;
				border-radius: 60px ;
				padding: 0 120px;
				color: #666;
				background: none;
				width: 100%;
				font-size: 14px;
				height: 60px ;
			}
			input::placeholder {
				color: #999;
				font-size: 14px;
			}
			button {
				border: 0px solid #e6e6e6;
				cursor: pointer;
				border-radius: 5px;
				padding: 0;
				margin: 0 0 0 10px;
				color: #fff;
				background: #0000FF;
				width: 120px;
				font-size: 15px;
				height: 60px ;
			}
			button:hover {
				opacity: 0.8;
			}
		}
		.register-btn {
			width: 100%;
		}
		.register-btn1 {
			margin: 40px 0;
			width: 100%;
		}
		.register-btn2 {
			width: 100%;
		}
		.r-btn {
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
		.r-btn:hover {
			border: 0px solid rgba(0, 0, 0, 1);
			opacity: 0.8;
		}
		.r-login {
			cursor: pointer;
			padding: 0;
			color: #000000;
			display: inline-block;
			text-decoration: none;
			width: 100%;
			font-size: 15px;
			line-height: 40px;
			text-align: center;
		}
		.r-login:hover {
			opacity: 1;
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
	::-webkit-scrollbar {
	  display: none;
	}
</style>
