INSERT INTO Users (username, last_name, first_name, email, password_hash, birth_date)
VALUES (
    'admin',
    'Demo',
    'Musify',
    'demo@musify.local',
    'gAAAAABqnY_oUYk_W8QtQeKz8_6GDjoK9mI6FotHp2esaArFH_m5LppiuWEzHJnDRSk8M2h6qRQB3LgI9KvNA29wZ8la0BO56Q==',
    '1998-01-01'
);

INSERT INTO Artists (artist_id, artist_name, genre, followers, profile_url, image) VALUES
(1, 'Eminem', 'Hip-Hop', 820000, 'https://www.youtube.com/channel/UCfM3zsQsOnfWNUppiycmBuw', 'https://yt3.googleusercontent.com/ytc/AIdro_ny_3E5NhElVE1msnq1HUwtnpjlV0JdXJ3h11Df2tlNmTQ=s160-c-k-c0x00ffffff-no-rj'),
(2, 'Drake', 'Hip-Hop', 900000, 'https://www.youtube.com/channel/UCByOQJjav0CUDwxCk-jVNRQ', 'https://yt3.googleusercontent.com/ytc/AIdro_lCPp6jFXJWIVHM0fIK5HofL3nyLOsmhu1Ek2OwyppYlOM=s160-c-k-c0x00ffffff-no-rj'),
(3, 'Lady Gaga', 'Pop', 750000, 'https://www.youtube.com/channel/UCNL1ZadSjHpjm4q9j2sVtOA', 'https://yt3.googleusercontent.com/PhFThrqp58joMS9FOd7I2jPZ1TepvCKDsdnuwmFXPl-Tq0kZjw3GNtCNtsxt3dgH8bqW7RdK=s160-c-k-c0x00ffffff-no-rj'),
(4, 'The Weeknd', 'R&B', 870000, 'https://www.youtube.com/channel/UC0WP5P-ufpRfjbNrmOWwLBQ', 'https://yt3.googleusercontent.com/WHvw1ak1FcJaHeEiTmG2iN0dqEjjPxAtT_tA8ruJ3MlNr9I-RHsAur1iAenYeQN_d6LNPH2Z8Ic=s160-c-k-c0x00ffffff-no-rj'),
(5, 'Imagine Dragons', 'Rock', 690000, 'https://www.youtube.com/channel/UCpx_k19S2vUutWUUM9qmXEg', 'https://yt3.googleusercontent.com/I0jhTGFbuG5MyNpnzo_tz0xUJ9hplyNFXA2tayDrmCT5nmjGzn4q5xgTwWHI0scboIc-yevr6qs=s160-c-k-c0x00ffffff-no-rj'),
(6, 'Adele', 'Pop', 1500000, 'https://www.youtube.com/user/AdeleVEVO', 'https://yt3.googleusercontent.com/vdfNWfvCReUf9wHOeC47JWmM1MbcAgnG12NXKi7VPxtmxIszk-S_DaeyNaB0NI3-pMoh1ZdNrw=s160-c-k-c0x00ffffff-no-rj');

INSERT INTO Songs (song_id, song_name, genre, release_date, url) VALUES
(1, 'Lose Yourself', 'Hip-Hop', '2002-10-28', 'https://www.youtube.com/watch?v=_Yhyp-_hX2s'),
(2, 'Without Me', 'Hip-Hop', '2002-05-13', 'https://www.youtube.com/watch?v=YVkUvmDQ3HY'),
(3, 'God''s Plan', 'Hip-Hop', '2018-01-19', 'https://www.youtube.com/watch?v=xpVfcZ0ZcFM'),
(4, 'Hotline Bling', 'Hip-Hop', '2015-07-31', 'https://www.youtube.com/watch?v=uxpDa-c-4Mc'),
(5, 'Bad Romance', 'Pop', '2009-10-26', 'https://www.youtube.com/watch?v=qrO4YZeyl0I'),
(6, 'Poker Face', 'Pop', '2008-09-26', 'https://www.youtube.com/watch?v=bESGLojNYSo'),
(7, 'Blinding Lights', 'R&B', '2019-11-29', 'https://www.youtube.com/watch?v=4NRXx6U8ABQ'),
(8, 'Radioactive', 'Rock', '2012-10-29', 'https://www.youtube.com/watch?v=ktvTqknDobU'),
(9, 'Hello', 'Pop', '2015-10-23', 'https://www.youtube.com/watch?v=YQHsXMglC9A'),
(10, 'Someone Like You', 'Pop', '2011-01-24', 'https://www.youtube.com/watch?v=hLQl3WQQoQ0');

INSERT INTO Albums (album_id, album_name, genre, release_date, cover_image) VALUES
(1, 'The Eminem Show', 'Hip-Hop', '2002-05-26', 'https://i.ytimg.com/vi/YVkUvmDQ3HY/hqdefault.jpg'),
(2, 'Scorpion', 'Hip-Hop', '2018-06-29', 'https://i.ytimg.com/vi/xpVfcZ0ZcFM/hqdefault.jpg'),
(3, 'The Fame', 'Pop', '2008-08-19', 'https://i.ytimg.com/vi/bESGLojNYSo/hqdefault.jpg'),
(4, 'After Hours', 'R&B', '2020-03-20', 'https://i.ytimg.com/vi/4NRXx6U8ABQ/hqdefault.jpg');

INSERT INTO Sings (artist_id, song_id) VALUES
(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10);

INSERT INTO Has (song_id, album_id) VALUES
(1, 1), (2, 1), (3, 2), (4, 2), (5, 3), (6, 3), (7, 4);

INSERT INTO Creates (artist_id, album_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4);

INSERT INTO Playlists (playlist_id, playlist_name, owner, private) VALUES
(1, 'Demo Hits', 'admin', FALSE),
(2, 'Late Night', 'admin', FALSE);

INSERT INTO ConsistsOf (playlist_id, song_id) VALUES
(1, 1), (1, 3), (1, 5), (1, 7), (1, 9),
(2, 4), (2, 6), (2, 8), (2, 10);

INSERT INTO LikedArtists (user_id, artist_id) VALUES
('admin', 1),
('admin', 3);

INSERT INTO LikedPlaylists (user_id, playlist_id) VALUES
('admin', 1);

INSERT INTO Likes (user_id, song_id) VALUES
('admin', 1),
('admin', 5),
('admin', 7);
