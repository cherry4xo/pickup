use std::sync::{Arc, RwLock};


struct User {
    id: i32
}

fn main() {
    let rw_user = RwLock::new(User { id: 1 });
    let static_user_ref: Arc<RwLock<User>> = Arc::new(rw_user);

    let threads = (0..3).map(|_| {
        let user_ref_copy: Arc<RwLock<User>> = static_user_ref.clone();
        std::thread::spawn(move || {
            let mut user = user_ref_copy.write().unwrap();
            user.id += 1;
        })
    });

    threads.map(|t| t.join()).for_each(drop);
    println!("{:?}", static_user_ref.read().unwrap().id);
}
