from flask import Flask ,render_template,request
import sqlite3
import joblib
import pandas as pd
import re
cosine_sim=joblib.load("./models/cosine_sim.lb")
df=pd.read_csv("movie_dataset.csv")
app = Flask(__name__) 
@app.route('/')  # http://127.0.0.1:5000/
def home(): 
    # return "Hii this is home page "
    return render_template('home.html')




@app.route('/recommend',methods=['GET','POST']) 
def recommend():
    recommendations=[]
    if request.method=='POST':
        def get_title_from_index(index):
           return df[df.index == index]["title"].values[0]
        def get_index_from_title(title):
    # Compile the regular expression pattern with case-insensitive flag
            pattern = re.compile(re.escape(title), re.IGNORECASE)
            
            # Apply the pattern to filter the DataFrame
            matching_indices = df[df['title'].apply(lambda x: bool(pattern.search(x)))].index
            
            # Return the first matching index if available
            if not matching_indices.empty:
                return matching_indices[0]
            else:
                return None 
        movie_user_likes=request.form["movie_name"]
        movie_index = get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
       
        # print("Top 5 similar movies to “+movie_user_likes+” are:\n")
        i=0
       
        for element in sorted_similar_movies:
            recommendations.append(get_title_from_index(element[0]))
            i=i+1
            if i>5:
                break
        
    return render_template('home.html',recommendations=recommendations)    


if __name__=="__main__":
    app.run(debug=True)            
   