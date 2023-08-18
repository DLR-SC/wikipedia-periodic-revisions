import dataclasses

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ast

from wikipedia_tools.processor import processor
from wikipedia_tools.utils import properties, utils
from tqdm import tqdm


@dataclasses.dataclass
class WikipediaRevisionAnalyzer:
    category: str = "Climate_change"
    only_popular: bool = False
    period: dict = dataclasses.field(
        default_factory=lambda:  properties.PERIODS._YEARLY_)
    corpus: str = properties.CORPUS
    root: str = properties.ROOT_PATH

    def __post_init__(self):
        self.CONSTANTS = properties._CONSTANTS_(self.root, self.corpus)
        self.periodic_df = processor.get_wikipedia_page_periodic_overview(
            only_popular=self.only_popular,
            period=self.period["format"],
            desc=self.period["description"],
            category=self.category,
            corpus=self.corpus,
            root=self.root
        )

    def get_edited_page_count(self, plot: bool = True, save: bool = False):
        dict_ = [
            {
                "period": period,
                "article_count": len(set(period_df["title"].unique())),
            }
            for period, period_df in self.periodic_df.groupby(["period"])
        ]

        unique_title_count_per_period: pd.DataFrame = pd.DataFrame(dict_)

        if plot:
            utils.barplot(
                "period",
                "article_count",
                unique_title_count_per_period,
                ylabel="Count of unique Wikipages",
                xlabel=self.period["description"].capitalize(),
                title="{}ly Count of Edited/Created {} Wikipedia Pages".format(
                    self.period["description"].capitalize(), self.category
                ),
            )

        if save:
            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            name = "{}ly_count_edited-and-created_wikipages.csv".format(
                self.period["description"].lower()
            )
            unique_title_count_per_period.to_csv(
                f"{self.CONSTANTS.STATS_FOLDER}/{name}"
            )
        return unique_title_count_per_period

    def get_created_page_count(
        self, plot: bool = True, save: bool = False
    ) -> pd.DataFrame:
        articles = []
        result = []
        for period_, df_ in self.periodic_df.groupby("period"):
            period_articles = df_["title"].unique().tolist()
            count_new_articles = len(
                [x for x in period_articles if x not in articles]
            )
            articles.extend(period_articles)
            if len(articles) == 0:
                print("error")
            row = {"period": period_, "new_article_count": count_new_articles}
            result.append(row)
        result_df = pd.DataFrame(result)
        if plot:
            utils.barplot(
                "period",
                "new_article_count",
                result_df,
                ylabel="Count of Created Wikipages",
                xlabel=self.period["description"].capitalize(),
                title="{}ly Count of Created {} Wikipedia Pages".format(
                    self.period["description"].capitalize(), self.category
                ),
            )

        if save:
            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            name = "{}ly_count_created_wikipages.csv".format(
                self.period["description"].lower()
            )
            result_df.to_csv(f"{self.CONSTANTS.STATS_FOLDER}/{name}")

        return pd.DataFrame(result)

    def get_revisions_over_time(
        self, plot: bool = True, save: bool = False
    ) -> pd.DataFrame:
        dict_ = [
            {"period": period_, "revision_count": df_["revision_count"].sum()}
            for period_, df_ in self.periodic_df.groupby(["period"])
        ]
        result_df = pd.DataFrame(dict_)

        if plot:
            utils.barplot(
                "period",
                "revision_count",
                result_df,
                ylabel="Count of Wikipage Revisions",
                xlabel=self.period["description"].capitalize(),
                title="{}ly Count of Wikipedia Revisions".format(
                    self.period["description"].capitalize()
                ),
            )
        if save:
            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            name = "{}ly_count_wikipedia_page_revisions.csv".format(
                self.period["description"].lower()
            )
            result_df.to_csv(f"{self.CONSTANTS.STATS_FOLDER}/{name}")
        return result_df

    def get_words_over_time(
        self, plot: bool = True, save: bool = False
    ) -> pd.DataFrame:
        self.periodic_df.sort_values(by="timestamp", inplace=True)

        pre_period_content_dict = {}
        result_arr = []

        for period_, df_ in self.periodic_df.groupby(["period"]):
            current_title_content = {
                row["title"]: str(row["content"]) for _, row in df_.iterrows()
            }
            pre_period_content_dict.update(current_title_content)

            period_word_num = {
                "period": period_,
                "word_count": sum(
                    [
                        len(v.split())
                        for _, v in pre_period_content_dict.items()
                    ]
                ),
            }
            result_arr.append(period_word_num)

        result_df = pd.DataFrame(result_arr)
        if plot:
            utils.barplot(
                "period",
                "word_count",
                result_df,
                ylabel="Count of Total Words",
                xlabel=self.period["description"].capitalize(),
                title="{}ly Wikipedia Page Word Count".format(
                    self.period["description"].capitalize()
                ),
            )
        if save:
            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            name = "{}ly_count_wikipedia_page_words.csv".format(
                self.period["description"].lower()
            )
            result_df.to_csv(f"{self.CONSTANTS.STATS_FOLDER}/{name}")

        return result_df

    def get_users_over_time(
        self, plot: bool = True, save: bool = False
    ) -> pd.DataFrame:
        result_arr = []
        over_time_anonymous = []
        over_time_registered = []
        for period_, df_ in self.periodic_df.groupby(["period"]):
            anonymous = []
            registered = []

            for user_lst_wiki in df_["users"].values.tolist():
                user_lst = ast.literal_eval(user_lst_wiki)

                anonymous.extend([x for x in user_lst if utils.is_ip(x)])
                registered.extend([x for x in user_lst if not utils.is_ip(x)])

            result_arr.append(
                {
                    "period": period_,
                    "count_edits": len(registered),
                    "count_unique_users": len(set(registered)),
                    "User Type": "Registered User",
                }
            )
            result_arr.append(
                {
                    "period": period_,
                    "count_edits": len(anonymous),
                    "count_unique_users": len(set(anonymous)),
                    "User Type": "Anonymous User",
                }
            )
            over_time_anonymous.extend(anonymous)
            over_time_registered.extend(registered)

        print(
            "Total of Unique Anonymous Users:  ", len(set(over_time_anonymous))
        )
        print(
            "Total of Unique Registered Users: ",
            len(set(over_time_registered)),
        )

        result_df = pd.DataFrame(result_arr)
        if plot:
            utils.barplot(
                "period",
                "count_edits",
                result_df,
                ylabel="Count of Revisions",
                xlabel=self.period["description"].capitalize(),
                title="{}ly edits count of Wikipedia Pages Per user type".format(
                    self.period["description"].capitalize()
                ),
                hue="User Type",
                dodge=True,
            )
            utils.barplot(
                "period",
                "count_unique_users",
                result_df,
                ylabel="Count of Unique Users",
                xlabel=self.period["description"].capitalize(),
                title="{}ly Count of Wikipedia Page Users".format(
                    self.period["description"].capitalize()
                ),
                hue="User Type",
                dodge=True,
            )

        if save:
            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            name = "{}ly_count_wikipedia_page_users.csv".format(
                self.period["description"].lower()
            )
            result_df.to_csv(f"{self.CONSTANTS.STATS_FOLDER}/{name}")
        return result_df

    def get_most_edited_articles(self, top: int = 5) -> pd.DataFrame:
        sns.set(font_scale=1)
        plt.style.use("fivethirtyeight")

        num_period = len(self.periodic_df["period"].unique())
        f, axes = plt.subplots(
            1, num_period, sharex=False, sharey=True, figsize=(20, 6)
        )

        idx = 0
        for period_, df_ in self.periodic_df.groupby(["period"]):
            top_titles_df = (
                df_[["title", "revision_count"]]
                .groupby("title")
                .sum()
                .sort_values(by="revision_count", ascending=False)
                .reset_index()[0:top]
            )

            ax = axes[idx]
            f.add_subplot(axes[idx])
            sns.barplot(
                x="title",
                y="revision_count",
                data=top_titles_df,
                color=sns.color_palette("PuBuGn_d", num_period)[idx],
            )

            # labels = [textwrap.fill(label.get_text(), 15) for label in ax.get_xticklabels()]
            # ax.set_xticklabels(labels)
            plt.gca().set_xticklabels(
                ax.get_xticklabels(), rotation=90, ha="right", fontsize=10
            )
            plt.gca().set_title(period_, fontsize=14)
            plt.gca().set_xlabel("")
            plt.gca().set_ylabel("")

            idx = idx + 1

        # plt.tight_layout()
        plt.subplots_adjust(wspace=1, hspace=2)
        plt.margins(x=0, y=0)
        # f.text(1, -0.32, 'Year', ha='center')
        f.text(
            0.5,
            1,
            "Top {} Titles per {}".format(
                top, self.period["description"].capitalize()
            ),
            ha="center",
            fontsize=16,
        )
        plt.show()

    def get_periodic_most_to_least_revised(
        self, plot: bool = True, save: bool = False
    ) -> pd.DataFrame:
        num_period = len(self.periodic_df["period"].unique())

        _dict = {}
        for period_, df_ in self.periodic_df.groupby(["period"]):
            sorted_titles = (
                df_[["title", "revision_count"]]
                .groupby("title")
                .sum()
                .sort_values(by="revision_count", ascending=False)
                .reset_index()
            )
            _dict[period_] = sorted_titles["title"].values.tolist()

        max = -1
        for _, v in _dict.items():
            max = len(v) if max < len(v) else max
        extended_dict = {
            k: v + ([""] * (max - len(v))) for k, v in _dict.items()
        }

        result_df = pd.DataFrame(extended_dict)
        if save:
            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            name = "{}ly_most-to-least_revised_wikipedia_pages.csv".format(
                self.period["description"].lower()
            )
            result_df.to_csv(f"{self.CONSTANTS.STATS_FOLDER}/{name}")
        return result_df

    def get_attr_for_period_as_txt(
        self,
        period_val: int | list,
        attr_val: str = "links",
    ):
        sns.set(font_scale=1)
        plt.style.use("fivethirtyeight")

        if type(period_val) == int:
            period_val = [period_val]
        res_dict = {}
        for single_period in tqdm(period_val):
            self._df = self.periodic_df[
                self.periodic_df["period"] == single_period
            ].copy()
            self._df.sort_values(
                by=["revision_count", "title"], inplace=True, ascending=False
            )

            result_arr = []
            for _, row in self._df.iterrows():
                lst_ = ast.literal_eval(row[attr_val])
                lst_ = [x.replace(" ", "") for x in lst_]
                if len(lst_) > 0:
                    result_arr.append(". ".join(lst_))

            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            with open(
                f"{self.CONSTANTS.STATS_FOLDER}/{attr_val}_{single_period}.txt",
                "w",
                encoding="utf-8",
            ) as f:
                for line in result_arr:
                    f.write(f"{line}\n")
            res_dict[single_period] = result_arr
        return res_dict

    def get_periodic_revisions_percentage(
        self,
        save: bool = False,
    ):
        self.periodic_df.sort_values(
            by=["period", "revision_count", "title"],
            inplace=True,
            ascending=False,
        )

        self.periodic_df["revision_percentage"] = round(
            100
            * self.periodic_df["revision_count"]
            / self.periodic_df.groupby("period")["revision_count"].transform(
                "sum"
            ),
            3,
        )
        result_df = self.periodic_df[
            [
                "period",
                "title",
                "revision_count",
                "revision_percentage",
                "timestamp",
            ]
        ]
        if save:
            utils.create_folder(self.CONSTANTS.STATS_FOLDER)
            name = "{}ly_wikipedia_page_revisions_w_percentage.csv".format(
                self.period["description"].lower()
            )
            result_df.to_csv(f"{self.CONSTANTS.STATS_FOLDER}/{name}")

        return result_df
