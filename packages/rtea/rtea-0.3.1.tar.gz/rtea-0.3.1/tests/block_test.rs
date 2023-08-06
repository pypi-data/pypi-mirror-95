//MAGIC
#[path = "../src/block.rs"]
mod block;
#[path = "../src/tea.rs"]
mod tea;

#[test]
#[cfg(debug_assertions)]
fn test_qqtea_encrypt() {
    let text: Vec<u8> = vec![0xff; 32];
    let key: Vec<u8> = vec![0xff; 16];
    let result: Vec<u8> = block::qqtea_encrypt(&text, &key);

    assert_eq!(
        result,
        vec![
            117, 61, 222, 94, 87, 182, 157, 64, 60, 2, 61, 98, 93, 16, 49, 145, 99, 99, 207, 164,
            26, 108, 72, 189, 100, 34, 27, 45, 206, 166, 44, 43, 157, 214, 172, 27, 75, 36, 27,
            106, 250, 218, 219, 132, 112, 70, 230, 241
        ]
    );
}
#[test]
#[cfg(debug_assertions)]
fn test_qqtea_decrypt() {
    let text: Vec<u8> = vec![
        117, 61, 222, 94, 87, 182, 157, 64, 60, 2, 61, 98, 93, 16, 49, 145, 99, 99, 207, 164, 26,
        108, 72, 189, 185, 227, 206, 205, 95, 210, 147, 25,
    ];
    let key: Vec<u8> = vec![0xff; 16];
    let result: Vec<u8> = block::qqtea_decrypt(&text, &key);

    assert_eq!(result, vec![0xff; 16]);
}

#[test]
fn test_qqtea_mixed() {
    let text: Vec<u8> = vec![0; 32];
    let key: Vec<u8> = vec![233; 16];

    let result = block::qqtea_decrypt(&block::qqtea_encrypt(&text, &key), &key);

    assert_eq!(text, result);
}
