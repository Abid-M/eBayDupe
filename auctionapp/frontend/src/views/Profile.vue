<template>
    <div class="container">
        <h1 class="text-center mb-5 display-5">Profile</h1>
        <div class="row">
            <div class="col-sm-8 offset-sm-2 col-md-6 offset-md-3 col-lg-4 offset-lg-4 display-6"> 
                <div class="profile-card rounded-lg shadow p-4 p-xl-5 mb-4 text-center position-relative">
                    <img class="imagePreviewWrapper" :src="editUser.profileImage" alt="My image">
                    <h3 class="mb-4">{{ editUser.username }}</h3>
                    <div class="text-left mb-4">
                        <p class="mb-2">{{ editUser.first_name }} {{ editUser.last_name }}</p>
                        <p class="mb-2">{{ editUser.dOB }}</p>
                        <p class="mb-2">{{ editUser.email }}</p>
                        <p class="mb-2" v-if='editUser.phoneNumber == null'></p>
                        <p class="mb-2" v-else>+44 {{ editUser.phoneNumber }}</p>
                        <hr>
                        <p class="mb-2">{{ editUser.addressLine1 }}</p>
                        <p class="mb-2">{{ editUser.addressLine2 }}</p>
                        <p class="mb-2">{{ editUser.postcode }}</p>
                        <p class="mb-2">{{ editUser.city }} , {{ editUser.country }}</p>
                    </div>
                    <div class="edit-profile-button justify-context-center">
                        <div class="popup" id="popup-2">
                            <div class="overlay"></div>
                            <div class="content">
                                <div class="close-btn" v-on:click="toggleImage()">&times;</div>
                                <h1>Edit Profile</h1>  
                                <form>
                                    <table style="width:100%"> <!-- Table to display details -->
                                        <tr>
                                            <td> <b>Profile Image</b> <input ref="fileInput" type="file" @input="onFileSelected" id="imageInput" class="form-control" placeholder="image"></td><br>
                                        </tr><br>
                                    </table>
                                </form>
                                <button @click="addImage(); toggleImage()" id="newupdate" class="btn btn-info">Save & Close</button>
                            </div>
                        </div>
                        <div class="popup" id="popup-1">
                            <div class="overlay"></div>
                            <div class="content">
                                <div class="close-btn" v-on:click="togglePopup()">&times;</div>
                                <h1>Edit Profile</h1>  
                                <form>
                                    <table style="width:100%"> <!-- Table to display details -->
                                        <tr>
                                        </tr><br>
                                        <tr>
                                            <td><b>Email</b><input type="email" id="email" class="form-control" placeholder="Email" v-model="editUser.email"></td> <br>                   
                                        </tr><br>
                                        <tr>
                                            <td><b>First Name</b><input type="text" id="first_name" class="form-control" placeholder="First Name" v-model="editUser.first_name" ></td>
                                            <td><b>Surname</b><input type="text" id="last_name" class="form-control" placeholder="Last Name" v-model="editUser.last_name"></td>                    
                                        </tr><br>
                                        <tr>
                                            <td><b>Date of Birth</b><input type="date" id="dOB" class="form-control" placeholder="Date Of Birth" v-model="editUser.dOB"></td>
                                            <td><b>Phone Number</b><input type="number" id="phoneNumber" class="form-control" placeholder="Phone Number" maxLength="11" v-model="editUser.phoneNumber"> </td>                  
                                        </tr><br>
                                        <tr>
                                            <td><b>Address Line 1</b><input type="text" id="addressLine1" class="form-control" placeholder="Address Line 1" v-model="editUser.addressLine1"></td>
                                            <td><b>Address Line 2</b><input type="text" id="addressLine2" class="form-control" placeholder="Address Line 2" v-model="editUser.addressLine2"></td>                    
                                        </tr><br>
                                        <tr>
                                            <td><b>City</b><input type="text" id="city" class="form-control" placeholder="City" v-model="editUser.city"></td>
                                            <td><b>Postcode</b><input type="text" id="postcode" class="form-control" placeholder="Postcode" v-model="editUser.postcode"></td>                   
                                        </tr><br>
                                        <tr>
                                            <td><b>Country</b><input type="text" id="country" class="form-control" placeholder="Country" v-model="editUser.country"></td>   
                                        </tr><br>
                                    </table>
                                </form>
                                <button @click="addImage(); editProfile(); togglePopup()" id="newupdate" class="btn btn-info">Save & Close</button>
                            </div>
                        </div>
                        <div class="edit-image-button">
                        <button type="button" class="btn btn-outline-secondary" v-on:click="toggleImage()">Edit Image</button>
                        </div>
                        <button type="button" class="btn btn-primary btn-lg" v-on:click="togglePopup()">Edit Profile</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    mounted(){
        this.getSpecificUser()
        
    },
    data() {
        return {
            loggedUser: [],
            editUser: {
                id:"",
                profileImage: null,
                username: "",
                email: "",
                first_name: "",
                last_name:"",
                dOB: "",
                phoneNumber:"",
                addressLine1:"",
                addressLine2:"",
                city:"",
                postcode:"",
                country:"",
            },

        }
    },
    methods:{

        selectImage() {
            this.$refs.fileInput.click();
            this.addImage() 
        },

        async addImage() {
            let formData = new FormData()
            formData.append('image', this.$refs.fileInput.files[0])

            console.log(formData)


            let response = await fetch(`http://localhost:8000/profileupdate/${this.editUser.id}/`, {
                method: "POST",
                body: formData       
            });

            this.getUpdatedProfile()
        },

        onFileSelected() {
            let input = this.$refs.fileInput
            let file = input.files

            if (file && file[0]) {
                let reader = new FileReader
                reader.onload = e => {
                    let hello = this.editUser.profileImage = e.target.result
                }
                reader.readAsDataURL(file[0])
                hello2 = this.$emit('input',file[0])
            }
        },

        async getSpecificUser() {
        let response = await fetch(`http://localhost:8000/api/account/`)
        let data = await response.json()

            this.loggedUser = data.SpecificUser;
            console.log(this.loggedUser[0].id)
            this.editUser.profileImage = this.loggedUser[0].profileImage;
            this.editUser.id = this.loggedUser[0].id;
            this.editUser.username = this.loggedUser[0].username;
            this.editUser.email = this.loggedUser[0].email;
            this.editUser.first_name = this.loggedUser[0].first_name;
            this.editUser.last_name = this.loggedUser[0].last_name;
            this.editUser.dOB = this.loggedUser[0].dOB;
            this.editUser.phoneNumber = this.loggedUser[0].phoneNumber;
            this.editUser.addressLine1 = this.loggedUser[0].addressLine1;
            this.editUser.addressLine2 = this.loggedUser[0].addressLine2;
            this.editUser.city = this.loggedUser[0].city;
            this.editUser.postcode = this.loggedUser[0].postcode;
            this.editUser.country = this.loggedUser[0].country;

            await this.getUpdatedProfile();

      },

    async getUpdatedProfile(){
        let response = await fetch(`http://localhost:8000/api/accounts/${this.editUser.id}/`,{
        method: 'GET'
        });
        let data = await response.json()
        this.loggedUser = data;

        this.editUser.profileImage = "http://localhost:8000" + this.loggedUser.profileImage;
        this.editUser.id = this.loggedUser.id;
        this.editUser.username = this.loggedUser.username;
        this.editUser.email = this.loggedUser.email;
        this.editUser.first_name = this.loggedUser.first_name;
        this.editUser.last_name = this.loggedUser.last_name;
        this.editUser.dOB = this.loggedUser.dOB;
        this.editUser.phoneNumber = this.loggedUser.phoneNumber;
        this.editUser.addressLine1 = this.loggedUser.addressLine1;
        this.editUser.addressLine2 = this.loggedUser.addressLine2;
        this.editUser.city = this.loggedUser.city;
        this.editUser.postcode = this.loggedUser.postcode;
        this.editUser.country = this.loggedUser.country; 
    },
    
    async editProfile(){
        var today = new Date()
        var editUserDOB = new Date(this.editUser.dOB)

        var strNumber = this.editUser.phoneNumber.toString();
        console.log(strNumber)

        if (!this.editUser.email.includes("@")) {
            alert("Please enter a valid email address!")
        }
        else if (editUserDOB > today) {
            alert("You can't be born in the future!")
        }
        else if (strNumber.length > 13) {
            alert("The number you entered is too long!")
        }
        else if (strNumber.length < 5) {
            alert("The number is too short!")
        }
        else if (this.editUser.dOB === "") {
            alert("You were born at some stage!")
        }else {
            let requestOptions = { 
                method: "PUT",
                body: JSON.stringify({
                    username: this.editUser.username,
                    email: this.editUser.email,
                    first_name: this.editUser.first_name,
                    last_name: this.editUser.last_name,
                    dOB: this.editUser.dOB,
                    phoneNumber: this.editUser.phoneNumber,
                    addressLine1: this.editUser.addressLine1,
                    addressLine2: this.editUser.addressLine2,
                    city: this.editUser.city,
                    postcode: this.editUser.postcode,
                    country: this.editUser.country,
                
                })
            };
            const response = await fetch (`http://localhost:8000/api/accounts/${this.editUser.id}/`, requestOptions);
            await this.getUpdatedProfile();
        }

    },
      togglePopup: function(){
        document.getElementById("popup-1").classList.toggle("active");
      },
      toggleImage: function(){
        document.getElementById("popup-2").classList.toggle("active");
      },
    }
};
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

.edit-image-button{
    width: 5px;
    height: 5px;
}

.imagePreviewWrapper {
    width: 225px;
    height: 225px;
    display: block;
    cursor: pointer;
    margin: 0 auto 30px;
    background-size: cover;
    background-position: center center;
}

body{
    color: #1a202c;
    background-color: #fff;    
}

.profile-card {
    box-shadow: 0 1px 3px 0 rgba(0,0,0,.1), 0 1px 2px 0 rgba(0,0,0,.06);
    font-size: large;
}
</style>