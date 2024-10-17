import numpy as np
import pandas as pd
import streamlit as st
from faker import Faker # type: ignore



@st.cache_data
def get_profile_dataset(number_of_items: int = 20, seed: int = 0) -> pd.DataFrame:
    new_data = []

    fake = Faker()
    np.random.seed(seed)
    Faker.seed(seed)

    for i in range(number_of_items):
        profile = fake.profile()
        new_data.append(
            {
                "name": profile["name"],
                "daily_activity": np.random.rand(25),
                "activity": np.random.randint(2, 90, size=12),
            }
        )

    profile_df = pd.DataFrame(new_data)
    return profile_df

