def rank_date(from_table = 'irae__gpt4_donor_vars', date_col = 'donor_date', group_ref = 'subject_ref', date_order = 'ASC'):

    sql = [f"WITH value_counts as (",
           f"select {group_ref}, {date_col}, count(*) as cnt",
           f"from {from_table}",
           f"where {date_col} is not null and {date_col} > date('2000-01-01')",
           f"group by {group_ref}, {date_col}", "),"
           f"ranked_tf as (",
           f"select {group_ref}, {date_col}, cnt,",
           f"row_number() over ( partition by {group_ref} order by cnt DESC, {date_col} {date_order}) as rn",
           "from value_counts )",
           f"SELECT {group_ref}, {date_col} as {date_col}_min from ranked_tf",
           f"where rn =1 order by {group_ref}"]
    return ' \n'.join(sql)

def rank_value(from_table = 'irae__gpt4_donor_vars', column ='donor_type', group_ref ='subject_ref', date_order ='ASC'):

    sql = [f"WITH value_counts as (",
           f"select {group_ref}, {column}, count(*) as cnt",
           f"from {from_table}",
           f"where {column} is not null",
           f"group by {group_ref}, {column}", "),"
           f"ranked_tf as (",
           f"select {group_ref}, {column}, cnt,",
           f"row_number() over ( partition by {group_ref} order by cnt DESC, {column} {date_order}) as rn",
           "from value_counts )",
           f"SELECT {group_ref}, {column} as {column}_min from ranked_tf",
           f"where rn =1 order by {group_ref}"]
    return ' \n'.join(sql)


if __name__ == "__main__":
    sql = rank_value(from_table='irae__gpt4_donor_vars', column='donor_type')
    print(sql)

