import pandas as pd
import numpy as np

class DiscountCurve:
    def __init__(self, curve_df: pd.DataFrame, day_count: int = 252):
        self.curve_df = curve_df.sort_values("days").reset_index(drop=True)
        self.day_count = day_count

    def discount_factor(self, days: int) -> float:
        curve_df = self.curve_df

        if days <= curve_df["days"].iloc[0]:
            return float(curve_df["discount_factor"].iloc[0])

        if days >= curve_df["days"].iloc[-1]:
            return float(curve_df["discount_factor"].iloc[-1])

        exact = curve_df[curve_df["days"] == days]
        if not exact.empty:
            return float(exact["discount_factor"].iloc[0])

        before = curve_df[curve_df["days"] < days].iloc[-1]
        after  = curve_df[curve_df["days"] > days].iloc[0]
        t0, t1 = before["year_frac"], after["year_frac"]
        d0, d1 = np.log(before["discount_factor"]), np.log(after["discount_factor"])
        t = days / self.day_count

        if t1 == t0:
            return float(np.exp(d0))

        d = d0 + (d1 - d0) * (t - t0) / (t1 - t0)

        return float(np.exp(d))

    def zero_rate_continuous(self, days: int) -> float:
        T = days / self.day_count
        df = self.discount_factor(days)
        return -np.log(df) / T

    def price_zero_coupon(self, face_value: float, days_to_maturity: int) -> float:
        df = self.discount_factor(days_to_maturity)
        return face_value * df


    def price_cashflows(self, cashflows):
        pv = 0.0
        for days, amount in cashflows:
            df = self.discount_factor(days)
            pv += amount * df
        return pv                   

    def price_fixed_rate_bond(
        self,
        face_value: float,
        coupon_rate: float,      
        years: int,
        payments_per_year: int = 1,) -> float:

        cashflows = []
        total_payments = years * payments_per_year
        coupon_per_payment = face_value * coupon_rate / payments_per_year

        for k in range(1, total_payments + 1):
            days = int(self.day_count * k / payments_per_year)
            if k < total_payments:
                amount = coupon_per_payment
            else:
                amount = coupon_per_payment + face_value  

            cashflows.append((days, amount))

        return self.price_cashflows(cashflows)


    def zero_curve_nodes(self) -> pd.DataFrame:
        df_nodes = self.curve_df.copy()
        df_nodes["zero_rate_cont"] = -np.log(df_nodes["discount_factor"]) / df_nodes["year_frac"]
        return df_nodes


