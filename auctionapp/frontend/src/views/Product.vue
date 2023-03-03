<template>
    <div class="container">
      <u><h1 class="text-danger" v-if="userItem.active == false">This Auction has Ended!</h1></u>
      <br>
      <button @click="deleteItem" class=" btn btn-danger" v-if="this.userItem.user_id == this.loggedUser">Delete your listing</button>
      <h1>{{ userItem.title }}</h1>
      <div class="row">
        <div class="col-md-4">
          <img class="img-fluid imagePreviewWrapper" :src="userItem.pictureOfItem" alt="My image">
        </div>
        <div class="col-md-7">
          <p><strong>Posted by:</strong> {{userItem.user}}</p>
          <p><strong>Category:</strong> {{ userItem.item_tag }}</p>
          <p><strong>Description:</strong> {{ userItem.description }}</p>
          <h3><strong>Starting Price:</strong> £{{ userItem.startingPrice }}</h3>
          <p><strong>Listing Created On:</strong> {{ userItem.startDateTimeItem }}</p>
          <p><strong>Time Left:</strong> {{ this.diffTimeLeft }} | {{ userItem.endDateTimeItem }}</p>
        </div>
        
      </div>
      
      <br>
      <div class="row">
        <div class="sui col-md-4">
          <h3 v-if="(this.currentbid == 0)"><strong>No Bids for this item yet!</strong></h3>
          <h3 v-else><strong>Current Bid:</strong> £{{this.currentbid}}</h3>
          <a @click="getItemBids(); togglePopup()"><p><strong>Total bids:</strong> [ <u class="text-primary" style="cursor: pointer" >{{this.totalbids}} bids</u> ]</p></a>
          <form @submit.prevent="this.addBid()">
            <div class="form-group col-sm-11">
              <label for="bidAmount">Enter your bid:</label>
              <input type="number" step="any" name="bid amount" id="bidAmount" class="form-control" v-model="userBid" required>
            </div>
            <i><p class="text-muted">Enter a bid more than the Starting Price & Current Bid</p></i>
            <button type="submit" class="btn btn-primary">Submit Bid</button>
          </form>
        </div>
        <div class="col-md-4">
            <h5>Questions</h5>
            <form @submit.prevent="this.addQuestion()">
                <div class="form-group col-sm-11">
                <label for="questionnw">Enter your Question:</label>
                <textarea class="form-control" id="questionnw" cols="50" rows="2" v-model="userQuestion" required></textarea>
                <br><button type="submit" class="btn btn-info">Submit Question</button>
                </div>
            </form>
        </div>
      </div>
      <br>
      <div class="row">
        <div class="col-md-6">  
                <h4>Q&A</h4>
                <h6 v-if="this.itemQuestions.length === 0">
                    No questions for this item yet!
                </h6>
                
                <p v-else v-for="(question,index) in itemQuestions.slice().reverse()" :key="index">
                    <strong>• {{question.user}}</strong> <br>
                    {{question.questionText}}<br>
                    <i><small>Posted on: {{question.dateTimeOfQuestion}}</small></i><br>
                    <br>
                    <i><b>Sellers answer:</b></i>
                    <div v-for="(answer,index) in itemAnswers.slice().reverse()" :key="index"> 
                        <div v-if="answer.questionID === question.id">
                         {{answer.answerText}}<br>
                         <i><small>Responded at: {{answer.dateTimeOfAnswer}}</small></i>
                        </div>
                    </div>

                    <div v-if="!itemAnswers.some(answer => answer.questionID === question.id)">
                        <form @submit.prevent="this.addAnswer(question, index)">
                            <label for="questionn">Answer here:</label><br>
                            <textarea name="questionn" id="questionn" cols="80" rows="2" v-model="sellerAnswer[index]" required></textarea><br>
                            <button type="submit" class="btn btn-dark">Submit Answer</button>
                        </form>
                        <br>
                    </div>

                    <hr>
                </p>  
         </div>
       </div>

      
    <div class="popup" id="popup-1">
        <div class="overlay"></div>
        <div class="content">
            <div class="close-btn" v-on:click="togglePopup()">&times;</div>
            <h1>Bidding History</h1>
            <u><h3>{{this.userItem.title}}</h3></u>
            <img class="img-fluid imageSmall" :src="userItem.pictureOfItem" alt="My image">
            <br>
            <br>
            <h5><b>Current Bid:</b> £{{this.currentbid}}</h5><h5><b>Total bids:</b> {{this.totalbids}}</h5><h6><b>Time left until:</b> {{this.userItem.endDateTimeItem}}</h6>
            <table class="table table-bordered">
            <thead>
              <tr>
                <th class="p-1 ">Bidder</th>
                <th class="p-1">Bid amount</th>
                <th class="p-1">Bid time</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="itemBid in itemBids.slice().reverse()">
                <td>{{itemBid.user}}</td>
                <td>£{{itemBid.bidAmount}}</td>

                <td>{{itemBid.dateTimeBids}}</td>

              </tr>
            </tbody>
          </table>
        </div>
    </div>
  </div>
  </template>

<script>
export default {
    name: "Product",
    data() {
        return {
            loggedUser: "",
            productId: "",
            userBid: "",
            userQuestion: "",
            sellerAnswer: [],
            currentbid: 0.0,
            totalbids: "0",
            userItem: {
            },
            itemBids:[],
            itemQuestions:[],
            itemAnswers: [],
            diffTimeLeft: ""
        };
    },
    created() {
        this.productId = this.$route.params.data
        this.getItem();
    },
    mounted() {
      this.getSpecificUser();  
    },

    methods: {
        async getSpecificUser() {
        let response = await fetch("http://localhost:8000/api/account/")
        let data = await response.json()
    

        this.loggedUser = data.SpecificUser[0].id
        console.log("this works", this.loggedUser)

        this.getItemBids();
        this.getHighestBid();
        this.getQuestions();
        this.getAnswers();
      },

      async getHighestBid() {
        let response = await fetch(`http://localhost:8000/getBids/${this.productId}/`)
            let data = await response.json()
            let bids = data.bids
            console.log(data)
            let highest = 0;
            let count = 0;

            for (let i = 0; i < bids.length; i++){
                let decimalNumber = parseFloat(bids[i].bidAmount)
                count++;

                if (decimalNumber > highest) {
                    highest = bids[i].bidAmount
                }
            }

            this.totalbids = count;
            this.currentbid = highest;
      },

        async getItem() {
            let response = await fetch(`http://localhost:8000/getItemDetail/${this.productId}/`,{
            method: 'GET'});

            let data = await response.json()
            this.userItem = data;
            this.userItem.pictureOfItem = "http://localhost:8000" + this.userItem.pictureOfItem 

            this.endDateStored = this.userItem.endDateTimeItem

            let getDate = this.userItem.endDateTimeItem
            let displayDate = new Date(getDate);
            let actualDate = displayDate.toLocaleString();
            this.userItem.endDateTimeItem = actualDate

            let getDate2 = this.userItem.startDateTimeItem
            let displayDate2 = new Date(getDate2);
            let actualDate2 = displayDate2.toLocaleString();
            this.userItem.startDateTimeItem = actualDate2

            this.calculate();
        },

        async getItemBids() {
            let response = await fetch(`http://localhost:8000/getBids/${this.productId}/`)
            let data = await response.json()
            this.itemBids = data.bids;

            for (let i = 0; i < this.itemBids.length; i++) {
                let getDate = this.itemBids[i].dateTimeBids
                let displayDate = new Date(getDate);
                let actualDate = displayDate.toLocaleString();

                this.itemBids[i].dateTimeBids = actualDate

            }
        },

        async addBid() {
            let response = await fetch(`http://localhost:8000/getBids/${this.productId}/`)
            let data = await response.json()
            let bids = data.bids;

            for (let i = 0; i < bids.length; i++) {
                let getDate = bids[i].dateTimeBids
                let displayDate = new Date(getDate);
                let actualDate = displayDate.toLocaleString();

                bids[i].dateTimeBids = actualDate

            }
            console.log(data)
            let highest = 0;

            for (let i = 0; i < bids.length; i++){
                let decimalNumber = parseFloat(bids[i].bidAmount)

                if (decimalNumber > highest) {
                    highest = bids[i].bidAmount
                }
            }

            console.log("This is the highest bid: ", highest)
            this.currentbid = highest

            let currentDate = new Date()
            currentDate = currentDate.toISOString();
            console.log("currentDate:")
            console.log(currentDate)

            console.log("saved enddate")
            console.log(this.endDateStored)

            if (this.userBid < this.userItem.startingPrice) {
                alert("Your bid needs to be equal to or greater than the Starting Price!")
            }

            else if(currentDate > this.endDateStored) {
                alert("This listing has ended so you cannot bid!")
            }

            else if (this.loggedUser === this.userItem.user_id){
                alert("You cannot bid on your own item!")
            }

            else if (this.userBid <= highest) {
                alert("Your Bid Amount needs to be higher then the current bid!")
            }
            else {
                await fetch(`http://localhost:8000/addBid/${this.productId}/`,{
                    method: 'POST',
                    body: JSON.stringify({
                        bidUser: this.loggedUser,
                        bidAmount: this.userBid,
                        bidTime: new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString()
                    })
                });
                alert("Bid Submitted!")
            }
            
            this.getHighestBid();
            this.userBid = "";
        },

        async getItemBids() {
            let response = await fetch(`http://localhost:8000/getBids/${this.productId}/`)
            let data = await response.json()
            this.itemBids = data.bids;


            for (let i = 0; i < this.itemBids.length; i++) {
                let getDate = this.itemBids[i].dateTimeBids
                let displayDate = new Date(getDate);
                let actualDate = displayDate.toLocaleString();

                this.itemBids[i].dateTimeBids = actualDate

            }
        },

        async addQuestion(){
            if (this.loggedUser === this.userItem.user_id) {
                alert("You cannot add a question on your own listing!")
            } else {

            await fetch(`http://localhost:8000/question/${this.productId}/`,{
                    method: 'POST',
                    body: JSON.stringify({
                        questionUser: this.loggedUser,
                        userQuestion: this.userQuestion,
                        questionTime: new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString()
                    })
                });
            alert("Question Submitted")
            this.getQuestions();
            }

        },

        async getQuestions() {
            let response = await fetch(`http://localhost:8000/question/${this.productId}/`)
            let data = await response.json()
            this.itemQuestions = data.questions;

            for (let i = 0; i < this.itemQuestions.length; i++) {
                let getDate = this.itemQuestions[i].dateTimeOfQuestion
                let displayDate = new Date(getDate);
                let actualDate = displayDate.toLocaleString();

                this.itemQuestions[i].dateTimeOfQuestion = actualDate

            }
        },

        async addAnswer(question, index){
            if (this.loggedUser !== this.userItem.user_id) {
                alert("Only the seller of this listing can answer questions!")
            } else{
            await fetch(`http://localhost:8000/answer/${this.productId}/`,{
                    method: 'POST',
                    body: JSON.stringify({
                        questionID: question.id,
                        sellerAnswer: this.sellerAnswer[index],
                        answerTime: new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString()
                    })
                });
            
                alert("Answer Submitted");
                this.getAnswers(question);
            }
 
        },

        async getAnswers() {
            let response = await fetch(`http://localhost:8000/answer/${this.productId}/`)
            let data = await response.json()
            this.itemAnswers = data.sellerAnswers;

            for (let i = 0; i < this.itemAnswers.length; i++) {
                let getDate = this.itemAnswers[i].dateTimeOfAnswer
                let displayDate = new Date(getDate);
                let actualDate = displayDate.toLocaleString();

                this.itemAnswers[i].dateTimeOfAnswer = actualDate

            }
        },

        async deleteItem(){
            let requestOptions = {
                method: "DELETE",
            };

            var confirm = window.confirm("Are you sure you want to delete?")

            if (confirm == true) {
                await fetch(`http://localhost:8000/getItemDetail/${this.productId}/`, requestOptions);
                alert("Item deleted")
                this.$router.push("/");
            }
        },

        calculate() {
            let currentDate = new Date()
            currentDate = currentDate.toISOString();
            currentDate = new Date(currentDate)

            let endDate = this.endDateStored
            endDate = new Date(endDate)


            let diff = Math.abs(endDate - currentDate);

            let days = Math.floor(diff / (1000 * 60 * 60 * 24));
            let hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

            if(this.userItem.active == true) {
                if (days > 0) {
                    this.diffTimeLeft = `${days}d ${hours}h ${minutes}m`;

                } else if (hours > 0) {
                    this.diffTimeLeft = `${hours}h ${minutes}m`;
                } else {
                    this.diffTimeLeft = `${minutes}m`;
                }   
            }   else {
                this.diffTimeLeft = "Ended"
            }
        },
        togglePopup: function(){
        document.getElementById("popup-1").classList.toggle("active");
      },
    }
};
</script>

<style>
.sui {
    width:33%
    
}

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
    width:450px;
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

.imageSmall {
    width: 100px;
    height: 100px;
    display: center;
    cursor: pointer;
    background-size: cover;
    background-position: center center;
}
</style>
