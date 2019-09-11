var vm = new Vue({
    el: '#app',
    data: {
        host,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
//        cart: [],
//        total_selected_count: 0,
//        origin_input: 0 // 用于记录手动输入前的值
    },
//    computed: {
//        total_count: function(){
//            var total = 0;
//            for(var i=0; i<this.cart.length; i++){
//                total += parseInt(this.cart[i].count);
//                this.cart[i].amount = (parseFloat(this.cart[i].price) * parseFloat(this.cart[i].count)).toFixed(2);
//            }
//            return total;
//        },
//        total_selected_amount: function(){
//            var total = 0;
//            this.total_selected_count = 0;
//            for(var i=0; i<this.cart.length; i++){
//                if(this.cart[i].selected) {
//                    total += (parseFloat(this.cart[i].price) * parseFloat(this.cart[i].count));
//                    this.total_selected_count += parseInt(this.cart[i].count);
//                }
//            }
//            return total.toFixed(2);
//        },
//        selected_all: function(){
//            var selected=true;
//            for(var i=0; i<this.cart.length; i++){
//                if(this.cart[i].selected==false){
//                    selected=false;
//                    break;
//                }
//            }
//            return selected;
//        }
//    },
    mounted: function(){
        // 获取购物车数据
        alert(this.user_id)
        if (this.user_id && this.token) {
//        alert("22222222222222222222222222")
            axios.get(this.host + '/projects/', {
                    // 向后端传递JWT token的方法
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                })
                .then(response => {
                    // 加载用户数据
                    this.user_id = response.data.id;
                    this.username = response.data.username;
//                    this.role_id =response.data.role_id
//                    alert(this.role_id)

                    // 补充请求浏览历史
                    axios.get(this.host + '/projects/', {
                            headers: {
                                'Authorization': 'JWT ' + this.token
                            },
                            responseType: 'json'
                        })
                        .then(response => {
                            alert("成功")
//                            this.histories = response.data;
//                            for(var i=0; i<this.histories.length; i++){
//                                this.histories[i].url = '/goods/' + this.histories[i].id + '.html';
//                            }
                        })
//
                })
                .catch(error => {
                    if (error.response.status==401 || error.response.status==403) {
                        location.href = '/login?next=/static/register.html';
                    }
                });
        } else {
            alert(1111)
            location.href = '/login?next=/register.html';
        }
    },
    methods: {
        // 退出
        logout: function(){
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
    }
});