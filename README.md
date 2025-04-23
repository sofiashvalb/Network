# Network Web App

**A full-featured social networking platform where users can create posts, follow other users, like content, and view a personalized feed. Built with Django and JavaScript, it offers a seamless and interactive user experience with real-time updates and single-page behavior.**

---

## Features

- **Create and Edit Posts** – Share thoughts and update them anytime
- **Like / Unlike Posts** – Show appreciation for posts with instant feedback
- **Follow / Unfollow Users** – Curate your own social space
- **Following Feed** – View posts from users you follow only
- **User Profiles** – Check out user activity, post history, and follower stats
- **Asynchronous Interactions** – Smooth and responsive UI without page reloads

---

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **Database:** SQLite (via Django ORM)
- **Authentication:** Django's built-in User model

---

## Highlights

- **Single Template, Multi-View Setup:**  
  All user interactions (posting, liking, following) happen on one dynamic template using show/hide logic in JavaScript

- **API-Driven Updates:**  
  Front-end JavaScript communicates with backend views via `fetch()` to keep everything responsive and in sync

- **Pagination:**  
  Posts are paginated for clean loading and navigation

- **Editable Posts:**  
  Users can edit their own content inline with immediate feedback

- **Modular Code:**  
  Clear separation of concerns between frontend logic and backend data management

