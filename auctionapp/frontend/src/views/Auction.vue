<template>
    <section style="padding:50px">
    <div class="container">  
        <form class="row g-3 mb-5 shadow p-4 border" @submit.prevent="createItem()">
            <div class="text-center"><h2 >Create Auction</h2></div>
            <div class="col-md-5">  
                <label for="title" class="form-label">Title</label>
                <input type="text" id="title" name="title" class="form-control" v-model="newItem.title" required>
            </div>
            <div class="col-md-3">
                <label for="category" class="form-label">Category</label><br>
                <select ref="selectInput" id="category" name="category" class="form-select" v-model="selectedOption">
                    <option v-for="option in options" :value="option.value">
                        {{ option.text }}
                    </option>
                </select>      
            </div>
            <div class="col-md-10">  
                <label for="description" class="form-label">Description</label>
                <textarea type="textfield" id="description" name="description" class="form-control" placeholder="Briefly describe your item..." rows="" v-model="newItem.description"></textarea>
            </div>
            <div class="col-md-3">
                <label for="startingPrice" class="form-label">Starting Price</label>
                <input type="number" step="any" id="startingPrice" name="startingPrice" class="form-control" v-model="newItem.startingPrice" required>
            </div>
            <div class="col-md-3">
                <label for="endDate" class="form-label">End Date</label>
                <input type="datetime-local" data-date-format="YYYY-MM-DD" id="endDate" name="endDate" max="2023-12-31" class="form-control" v-model="newItem.endDate" required>
            </div>
            <div class="col-md-3">  
                <label class="form-label">Image</label> 
                <input ref="fileInput" type="file" id="imageInput" class="form-control" placeholder="image" required>
            </div>
            <div class="col-md-12">  
                <input class="btn btn-primary" type="submit" value="Post">
            </div>
        </form>
    </div>
    <!-- <button @click="createItem">Submit</button><br> -->
    <h2 v-if="(this.userItems.length === 0)"></h2>
    <div v-else>
        <h2>Your Current Listings</h2>
        <i><small>Click item title to view product details</small></i>
        <br>
        <br>
        <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <th class="p-1 ">Category</th>
                <th class="p-1">Title</th>
                <th class="p-1">Description</th>
                <th class="p-1">Start Price</th>
                <th class="p-1">Start Date</th>
                <th class="p-1">End Date</th>
                <th class="p-1">Is active</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(userItem, index) in userItems.slice().reverse()" :key="index">
                <td>{{userItem.item_tag}}</td>
                
                <td>
                    <u>
                        <a @click="shareData(userItem)">
                            <td style="cursor: pointer" class="text-primary">{{userItem.title}}</td>
                        </a>
                    </u>
                </td>

                <td>{{userItem.description}}</td>
                <td>£{{userItem.startingPrice}}</td>
                <td>{{userItem.startDateTimeItem}}</td>
                <td>{{userItem.endDateTimeItem}}</td>
                <td>{{userItem.active}}</td>
            </tr>
            </tbody>
        </table>
    </div>
</section>
</template>

<script>
export default{
    mounted(){
        this.getSpecificUser() 
    },
    data() {
        return {
            loggedUser:"",
            userItems:[],
            newItem: {
                id:"",
                category:"",
                pictureOfItem: "",
                title:"",
                description:"",
                startingPrice: 0.0,
                startDate:"",
                endDate:"",
            },

            selectedOption: null,
            options: [
                { value: 'Sports', text: 'Sports'},
                { value: 'Technology', text: 'Technology'},
                { value: 'Clothes', text: 'Clothes'},
                { value: 'Kitchen', text: 'Kitchen'},
            ]
        }
    },
    methods:{
        async createItem(){
            let formData = new FormData()
            
            formData.append('image', this.$refs.fileInput.files[0])
            formData.append('category', this.selectedOption)
            formData.append('title', this.newItem.title)
            formData.append('description', this.newItem.description)
            formData.append('startingPrice', this.newItem.startingPrice)
            formData.append('startDate', new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString())
            formData.append('endDate', this.newItem.endDate)
            

            console.log (formData.get('endDate'))
            console.log (formData.get('startDate'))

            const now = new Date()
            const endDate = new Date(this.newItem.endDate)
            const startPrice = this.newItem.startingPrice
            if(startPrice<= 0){
                alert("You must enter a value created than £0")
            }
            else if (endDate < now) {
                alert("Your End Date can't be in the past!")
            } 
            else {
                await fetch(`http://localhost:8000/item/${this.loggedUser}/`,{
                    method: "POST",
                    body: formData
                })
            alert("Listing Created")
            this.userListings();
            }

            this.newItem.id = "",
            this.newItem.category = "",
            this.selectedOption = null,
            this.$refs.selectInput.selectedIndex = -1
            this.newItem.pictureOfItem= "",
            this.$refs.fileInput.value = null
            this.newItem.title="",
            this.newItem.description="",
            this.newItem.startingPrice= 0.0,
            this.newItem.startDate="",
            this.newItem.endDate=""

        },
        async getSpecificUser() {
        let response = await fetch("http://localhost:8000/api/account/")
        let data = await response.json()
    

        this.loggedUser = data.SpecificUser[0].id
        console.log("this works", this.loggedUser)
        this.userListings() 
      },
        async getSpecificUser() {
        let response = await fetch("http://localhost:8000/api/account/")
        let data = await response.json()
    

        this.loggedUser = data.SpecificUser[0].id
        console.log("this works", this.loggedUser)
        this.userListings() 
      },
    
      async userListings(){
        let response = await fetch(`http://localhost:8000/item/${this.loggedUser}/`)
        let data = await response.json()
        this.userItems = data.item;
        console.log(data)
        

        for (let i = 0; i < this.userItems.length; i++) {
            let getDate = this.userItems[i].endDateTimeItem
            let displayDate = new Date(getDate);
            let actualDate = displayDate.toLocaleString();

            this.userItems[i].endDateTimeItem = actualDate

        }

        for (let i = 0; i < this.userItems.length; i++) {
            let getDate = this.userItems[i].startDateTimeItem
            let displayDate = new Date(getDate);
            let actualDate = displayDate.toLocaleString();

            this.userItems[i].startDateTimeItem = actualDate
        }
     },

     shareData(userItem) {
        console.log(userItem)
        console.log(" ")
        this.$router.push({ name: 'Product', params: {data: userItem.id}});
     }
    }
}
</script>