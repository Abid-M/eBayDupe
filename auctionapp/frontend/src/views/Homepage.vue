<template>
    <section style="padding: 25px;">
    <p>Signed in as <b>{{ username }}</b></p> <!-- Only gets the username of that specific account -->

    <div class="popup" id="popup-1">
        <div class="overlay"></div>
        <div class="content">
            <div class="close-btn" v-on:click="togglePopup(); reset()">&times;</div>
            <div>
                <h2>Search for Item: </h2>
                <form ref="searchBar">
                    <input type='text' ref="searchBar" class="input" name="query" v-model="query" placeholder="Enter your keyword">
                </form> 
                <div class="col-md-12 text-center">                 
                    <button class="" @click="performSearch()">Search</button>
                    </div>

                    <form ref="results">
                     <table>   
                        <tr class="border-bottom">
                            <tr v-for="item in items" v-bind:key="item.item_title">
                            <td><img class="imagePreviewWrapper" @click="shareData(item)" :src="item.image" alt="My image"></td>
                            <u>
                                <a @click="shareData(item)">
                                        <td class="text-primary" style="cursor: pointer">{{item.title}}</td>
                                    </a>
                                </u>
                            <tr>
                                <td>Starting Price: £{{item.startingPrice}}</td>

                            </tr>
                            <tr>
                                <td>Listed by: {{item.listedUser}}</td>              
                            </tr>
                            </tr>
                   
                        </tr>
                    </table>
                    </form>
                </div>
            <button @click="togglePopup()" id="newupdate" class="btn btn-info">Close</button>
        </div>
    </div>
<button v-on:click="togglePopup()">Search Item</button>


        <!-- <table> -->

                    <div class="items" style="margin:0 auto; margin-bottom: 25px;" v-for="displayItem in displayItems"> 
                    <img class="imagePreviewWrapper image" @click="shareData(displayItem)" :src="displayItem.pictureOfItem" alt="Item image">
                    <div class="details">
                        <u>
                            <a @click="shareData(displayItem)">
                                <td class="text-primary" style="cursor: pointer">{{displayItem.title}}</td>
                            </a>
                        </u>
                            <br>
                                Starting Price: £{{displayItem.startingPrice}}
                            <br>
                            Listed by: {{displayItem.user}}
                            <br>
                            <div v-if="displayItem.active == false">
                                <br>
                                <strong class="text-danger">Auction has Ended!</strong>   
                            </div>
                    </div>
                    <br>
                </div>
</section>
</template>

<script>
export default{
    mounted(){
        this.getSpecificUser(),
        this.listings()
    },
    data() {
        return {
            loop: 0,
            loggedUser: [],
            username: "",
            displayItems:[],
            title:"",
            startingPrice:0,
            user:"",
            query:"",
            items: [],
            item: {
                title : "",
            }
        }
    },
    methods:{
        async getSpecificUser() {
        let response = await fetch("http://localhost:8000/api/account/")
        let data = await response.json()
        this.loggedUser = data.SpecificUser;
        this.username = this.loggedUser[0].username;
        this.id = this.loggedUser[0].id;
      },
      async listings(){
        let response = await fetch(`http://localhost:8000/displayItems/`)
        let data = await response.json()
        this.displayItems = data.AllItems;
        this.title = this.displayItems.title;
        this.startingPrice = this.displayItems.startingPrice;
        this.user = this.displayItems.user;

        console.log(this.displayItems)

        for (let i = 0; i < this.displayItems.length; i++) {
            this.displayItems[i].pictureOfItem = "http://localhost:8000" + this.displayItems[i].pictureOfItem
        }
    },

    async performSearch(){

        var data = {
            'query': this.query,
        }

        let response = await fetch("http://localhost:8000/search/",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        let result = await response.json();
        console.log(result.items);
        this.items = result.items;

        for(let i =0; i<this.items.length; i++) {
            this.items[i].image = "http://localhost:8000" + this.items[i].image
        }
        this.$refs.searchBar.clear();

    },
    async fetchItems() {
            let response = await fetch("http://localhost:8000/displayItems/")
            let data = await response.json()
            this.items = data.items
    },


    shareData(displayItem) {
        console.log(displayItem)
        console.log(" ")
        this.$router.push({ name: 'Product', params: {data: displayItem.id}});
     },

     togglePopup: function(){
        document.getElementById("popup-1").classList.toggle("active");
        this.$refs.searchBar.reset();
        this.items = [];
        this.reset()
      },
      reset: function(){
        this.$refs.searchBar.clear();
        this.items = [];
      },
  }
}

</script>
<style>
.popup .overlay{
    position:fixed;
    top:0px;
    left:0px;
    width:100vw;
    height:100vh;
    background:rgba(0,0,0,0.9);
    z-index:1;
    display:none;

}

.popup .content{
    position:absolute;
    top:50%;
    left:50%;
    transform: translate(-50%, -50%) scale(0);
    background: #fff;
    width:650px;
    height:fit-content;
    z-index:2;
    text-align: center;
    padding:20px;
    box-sizing:border-box;


}

.popup .close-btn{
	cursor:pointer;
    position:absolute;
    right:20px;
    top:20px;
    width: 30px;
    height: 30px;
    color: #222;
    font-size:20px;
    font-weight: 600;
    line-height: 28px;
    text-align: center;

}

.popup.active .overlay{
    display:block;
}

.popup.active .content{
    transition:all 100ms ease-in-out;
    transform: translate(-50%, -50%) scale(1);
}


.imagePreviewWrapper {
    width: 250px;
    height: 250px;
    display: block;
    cursor: pointer;
    background-size: cover;
    background-position: center center;
}


.image {
   float:left;
   width: 30%;
   height: 100%;
}

.details {
   float: left;
   width: 60%;
   height: 90%;
   padding-top: 20px;
   padding-left: 20px;
   margin-left: 20px;
}

.items {
    border: solid black 1px;
    margin: 100%;
    height: 280px;
    width: 50%;
    justify-content: center;
}

.padding {
    margin:150px;
}



</style>

