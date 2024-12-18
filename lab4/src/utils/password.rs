use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2
};

#[tracing::instrument(name = "Hashing user password", skip(password))]
pub async fn hash(password: &[u8]) -> String {
    let salt = SaltString::generate(&mut OsRng);
    Argon2::default()
        .hash_password(password, &salt)
        .expect("Unable to hash password")
        .to_string()
}

#[tracing::instrument(name = "Verifying user password", skip(password, hash))]
pub fn verify_password(password: &[u8], hash: &str) -> Result<(), argon2::password_hash::Error> {
    let hash = PasswordHash::new(&hash)
        .map_err(|e| println!("hash error: {}", e)).unwrap();

    let res = Argon2::default().verify_password(password, &hash);

    match res {
        Ok(_) => Ok(()),
        Err(err) => {
            println!("verify error {}", err.to_string());
            Err(argon2::password_hash::Error::Crypto)
        }
    }
}