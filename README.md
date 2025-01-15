# Smart Budget Planner
#### Video Demo:  (https://youtu.be/n6P-4ZfujZQ)
#### Description:
It's a web application designed to help users manage their finances effectively. This app is meant to help users to take control of their budgets, save strategically, and even explore investment opportunities through stock tracking.
The key features of this app includes:
- User registration and login: To ensure that all personal financial data is private. User sessions are managed effectively using Flask-Session.
- Budgeting Interface: This is where the user can enter their monthly income (in the form of 2 sperate paychecks), monthly expenses and finally get a summary after subimitting the budget. If the user has a remaining budget, they may choose invest it either in our very savings account, the stock market, both, or neither.
- Savings Page: Here the user can choose to invest any amount of the remaining budget they prefer. Savings grow automatically at an annual rate of 4.5%, allowing users to simulate their investments.
- Stock Tracking Page: User can simple enter stock symbols and number of shares they would like to purchase. Financcial data is provided through the cs50 finance API
- Insights Page: This is meant to be a page for "premium" users to get a visual view of their spending habits and change in income and spending over time. Non-premium users can click a button to enjoy a "free 7-day trial" in which when pressed, the user can enjoy some lighthearted fun by being redirected to a random YouTube video
##### Files written and their Purpose
- app.py: The core of my project. Manages routes, handles requests, and renders templates. It’s basically the backbone connecting all features and functionalities.
- helpers.py: A utility script containing helper functions such as:
1. apology: Renders error messages.
2. login_required: A decorator to make sure access to certain pages are only for logged-in users.
3. lookup: Queries the financial API for stock data.
4. usd: Formats values as USD currency
- Frontend Templates (in /templates)
1. layout.html: The base template for consistent design throught the site. Other templates extend from this file.
2. index.html: The homepage showcasing key features and navigation options.
3. budget.html: This consists of the form where users input their income and expenses.
4. savings.html: The page where users can choose to invest in our savings account and simulate investments.
5. stocks.html: Allows users to purchase/sell stocks and view their stock portfolio.
6. apology.html: Displays error messages to users in a friendly way using memegen.link.
7. signup.html and signin.html: Registration and login pages for secure user access.
8. sell.html: Manages selling of stocks.
9. insights.html: Users can "view" their insights but it's just some lighthearted fun
10. aboutus.html: Self-explanatory:D
11. careers.html: Users who would like to work with us can simply fill in a form
- Static Files (in /static)
1. styles.css: My own custom CSS to style the application that works alongside Bootstrap for a clean and modern look.
2. Several images including logos, icons, and visuals for enhancing the site's appearance
- fintracker.db: The SQLite database that consists of 5 tables to store user data
1. User information (credentials and sessions).
2. Budget details (income and expenses).
3. Savings and stock interactions (in 2 seperate tables).
4. Table to store data that was entered through careers.html
- The database schema was designed to optimize storage and retrieval efficiency. Tables were normalized to reduce redundancy, and meaningful relationships were established between users, budgets, and investments.
##### Design Choices
- Backend with Flask: I chose Flask for its simplicity and lightweight nature, which is perfect for a project of this scale. Its flexibility helps with seamless integration of user authentication, database management and dynamic routing.
- User Interface: The UI was designed with a focus on modern design principles while keeping it simple enough for users to navigate effortlessly. Bootstrap classses were also used to enhance aesthetics,
##### Challenges Faced and Solutions
- Deciding on what project to make was probably a challenge lol. Out of all the psets, the finance one was my favorite since I find the stock market pretty interesting, which is why I decided to do a project related to finance.
- At first, I struggled with customizing the appearance of the site using Bootstrap since it's not something I'm familiar with. Using ChatGPT, I learned how to use their classes effectively to create a visually appealing and functional design.
